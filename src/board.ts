import * as vscode from 'vscode';
import { SerialPort } from 'serialport';
import { PortInfo } from '@serialport/bindings-cpp';
import { Logger } from './logger';
import MicroPythonBoard from './micropython';
import { StubsManager } from './stubs';

export class DeviceManager {
    // 私有字段
    private _statusBarItem: vscode.StatusBarItem;
    private _currentPort?: string;
    private _logger: Logger;
    private _board: MicroPythonBoard | null = null;
    private _isConnecting = false;
    private _dataListener?: (line: string) => void;
    private _replPanel?: any;
    private _isHardReset: boolean = false;
    private _currentBoard: string = '未知开发板';
    private _boardStatusBarItem: vscode.StatusBarItem;
    private _stubsManager: StubsManager;

    // 私有方法
    private _updateStatusBar() {
        if (this._currentPort) {
            const isConnected = this.isConnected();
            const icon = isConnected ? '$(plug)' : '$(circle-slash)';
            this._statusBarItem.text = `${icon} ${this._currentPort}`;
            this._statusBarItem.tooltip = isConnected ? '设备已连接' : '设备未连接，点击重新连接';
        } else {
            this._statusBarItem.text = '$(circle-slash) 未选择串口';
            this._statusBarItem.tooltip = '点击选择串口设备';
        }
    }

    private _updateBoardStatusBar() {
        this._boardStatusBarItem.text = `$(device-desktop) ${this._currentBoard}`;
    }

    private _handleSerialClosed() {
        this._logger.debug('[串口]连接已关闭');
        this._board?.serial?.removeAllListeners('data');
        this._board?.serial?.removeAllListeners('close');
        this._replPanel?.setStatus?.('未连接', false);
        this._updateStatusBar();
        this._board = null;
        if (this._isHardReset) {
            this._isHardReset = false;
            setTimeout(() => {
                this.reconnect().catch(err => {
                    this._logger.warn('硬重启后自动重连失败: ' + (err instanceof Error ? err.message : String(err)));
                });
            }, 800);
        } else {
            this._currentPort = undefined;
        }
    }

    // 构造函数
    constructor(logger: Logger, replPanel?: any, context?: vscode.ExtensionContext) {
        this._logger = logger;
        this._replPanel = replPanel;
        this._stubsManager = new StubsManager(context!, logger);
        this._boardStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 101);
        this._boardStatusBarItem.command = 'extension.selectBoard';
        this._boardStatusBarItem.tooltip = '点击选择开发板';
        this._boardStatusBarItem.show();
        this._updateBoardStatusBar();
        this._statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this._statusBarItem.command = 'extension.mpyStatusBarConnect';
        this._updateStatusBar();
        this._statusBarItem.show();
    }

    async loadConfig(context: vscode.ExtensionContext) {
        try {
            // 获取当前开发板名称
            this._currentBoard = await this._stubsManager.getCurrentBoard();
            this._updateBoardStatusBar();
        } catch (error) {
            this._currentBoard = '未知开发板';
            this._updateBoardStatusBar();
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`加载开发板配置失败: ${errorMsg}`);
        }
    }

    // 公共方法
    async _listPorts(): Promise<string[]> {
        try {
            const ports = await SerialPort.list();
            this._logger.debug('扫描串口: ' + JSON.stringify(ports, null, 2));
            return ports.filter((portInfo: PortInfo) => {
                if (!portInfo?.path) return false;
                const path = portInfo.path.toLowerCase();
                return path.includes('usbserial') || path.includes('usbmodem') ||
                    path.includes('slab_usbtouart') || path.includes('ttyusb') ||
                    path.includes('ttyacm') || /^com\d+/.test(path);
            }).map((portInfo: PortInfo) => portInfo.path);
        } catch (error) {
            this._logger.warn(`串口扫描错误: ${error instanceof Error ? error.message : String(error)}`);
            return [];
        }
    }

    async selectPort(port?: string): Promise<string | undefined> {
        if (!port) {
            const ports = await this._listPorts();
            if (ports.length === 0) {
                vscode.window.showWarningMessage('无可用的MPY设备串口');
                return undefined;
            }
            const selection = await vscode.window.showQuickPick(ports, {
                placeHolder: '选择MPY设备串口'
            });
            if (!selection) return undefined;
            port = selection;
        }
        this._currentPort = port;
        this._updateStatusBar();
        this._logger.debug(`选择端口: ${port}`);
        return port;
    }

    async connect(): Promise<void> {
        let port = this._currentPort;
        if (!port) {
            const ports = await this.selectPort();
            port = this._currentPort;
            if (!port) throw new Error('未选择串口设备');
        }
        if (this.isConnected() && this._currentPort === port) {
            return;
        }
        if (this._isConnecting) {
            throw new Error('正在连接中...');
        }
        this._isConnecting = true;
        try {
            if (!this._board) {
                this._board = new MicroPythonBoard();
            }
            await this._board.open(port);
            this._replPanel?.setStatus?.(`已连接: ${port}`, true);
            if (this._dataListener) this._board.parser?.removeListener('data', this._dataListener);
            this._dataListener = (line: string) => {
                this._replPanel?.addOutput?.(line, 'output');
            };
            this._board.parser?.on('data', this._dataListener);
            this._board.serial?.on('close', () => this._handleSerialClosed());
            try {
                await Promise.race([
                    this._board.get_prompt(),
                    new Promise((_, reject) => setTimeout(() => reject(new Error('握手超时')), 3500))
                ]);
            } catch (handshakeError) {
                this._logger.debug(`握手校验失败: ${handshakeError instanceof Error ? handshakeError.message : String(handshakeError)}`);
                throw new Error('设备无响应，连接失败');
            }
            this._currentPort = port;
            this._logger.info(`已连接到端口 ${port}`);
            this._isConnecting = false;
            this._updateStatusBar();
        } catch (error) {
            this._logger.warn(`连接失败: ${error instanceof Error ? error.message : String(error)}`);
            if (this._board) {
                try { await this._board.close(); } catch { }
                this._board = null;
            }
            throw error;
        } finally {
            this._isConnecting = false;
        }
    }

    async reconnect(): Promise<void> {
        let port = this._currentPort;
        if (!port) {
            const ports = await this.selectPort();
            port = this._currentPort;
            if (!port) throw new Error('未选择串口设备');
        }
        if (this.isConnected() && this._currentPort === port) {
            return;
        }
        if (this._isConnecting) {
            throw new Error('正在连接中...');
        }
        this._isConnecting = true;
        try {
            if (!this._board) {
                this._board = new MicroPythonBoard();
            }
            await this._board.open(port);
            this._replPanel?.setStatus?.(`已连接: ${port}`, true);
            if (this._dataListener) this._board.parser?.removeListener('data', this._dataListener);
            this._dataListener = (line: string) => {
                this._replPanel?.addOutput?.(line, 'output');
            };
            this._board.parser?.on('data', this._dataListener);
            this._board.serial?.on('close', () => this._handleSerialClosed());
            this._currentPort = port;
            this._logger.info(`已连接到端口 ${port}`);
            this._isConnecting = false;
            this._updateStatusBar();
        } catch (error) {
            this._logger.warn(`连接失败: ${error instanceof Error ? error.message : String(error)}`);
            if (this._board) {
                try { await this._board.close(); } catch { }
                this._board = null;
            }
            throw error;
        } finally {
            this._isConnecting = false;
        }
    }

    async disconnect(): Promise<void> {
        if (this._dataListener && this._board) {
            this._board.parser?.removeListener('data', this._dataListener);
            this._dataListener = undefined;
        }
        if (this._board) {
            try {
                await this._board.close();
                this._handleSerialClosed();
            } catch (error) {
                this._logger.warn(`断开串口错误:${error instanceof Error ? error.message : String(error)}`);
            }
        }
    }

    async getPrompt(): Promise<string> {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.get_prompt() as string;
    }

    async run(code: string): Promise<string> {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.run(code) as string;
    }

    isConnected(): boolean {
        return !!(this._board && this._board.serial && this._board.serial.isOpen);
    }

    getCurrentPort(): string | undefined {
        return this._currentPort;
    }

    clearPort() {
        this._currentPort = undefined;
        this._updateStatusBar();
    }

    getStubsManager(): StubsManager {
        return this._stubsManager;
    }

    async sendCommand(command: string): Promise<void> {
        if (!this._board) throw new Error('设备未连接');
        try {
            this._logger.debug(`发送命令: ${command}`);
            if (this._board.serial && this._board.serial.isOpen) {
                await this._board.eval(command);
            } else {
                throw new Error('串口未打开');
            }
        } catch (error) {
            this._logger.warn(`发送命令失败: ${error instanceof Error ? error.message : String(error)}`);
            throw error;
        }
    }

    async fs_put(src: string, dest: string, data_consumer?: (msg: string) => void) {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.fs_put(src, dest, data_consumer);
    }

    async hard_reset() {
        if (!this._board) throw new Error('设备未连接');
        this._isHardReset = true;
        await this._board.get_prompt();
        await this._board.enter_raw_repl();
        await this._board.exec_raw("import time, machine; time.sleep_ms(100); machine.reset()\n");
    }

    async fs_rm(filePath: string) {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.fs_rm(filePath);
    }

    dispose() {
        this._statusBarItem?.dispose();
        this._boardStatusBarItem?.dispose();
        this._board?.close();
    }
} 