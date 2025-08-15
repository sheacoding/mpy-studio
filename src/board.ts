import * as vscode from 'vscode';
import { SerialPort } from 'serialport';
import { Logger } from './logger';
import MicroPythonBoard from './micropython';
import { StubsManager } from './stubs';
import { DeviceFolder } from './deviceFloder';
import * as path from 'path';

export class DeviceManager {
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
    private _deviceFolder?: DeviceFolder;
    private _context: vscode.ExtensionContext;
    private openFileMap = new Map<string, string>();

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
        vscode.commands.executeCommand('setContext', 'mpyStudio.deviceConnected', false);
        if (this._isHardReset) {
            this._isHardReset = false;
            this._logger.debug('硬重启完成，等待设备启动...');
            // 延长等待时间，确保设备完全重启
            setTimeout(async () => {
                try {
                    this._logger.debug('尝试硬重启后重连...');
                    await this.reconnect();
                    this._logger.info('硬重启后自动重连成功');
                } catch (err) {
                    this._logger.warn('硬重启后自动重连失败: ' + (err instanceof Error ? err.message : String(err)));
                    // 重连失败时清除端口，避免后续问题
                    this._currentPort = undefined;
                    this._updateStatusBar();
                }
            }, 1200); // 增加到1.2秒
        } else {
            this._currentPort = undefined;
        }
    }

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
        this._context = context!;
    }

    async loadConfig(context: vscode.ExtensionContext) {
        try {
            this._currentBoard = await this._stubsManager.getCurrentBoard();
            this._updateBoardStatusBar();
        } catch (error) {
            this._currentBoard = '未知开发板';
            this._updateBoardStatusBar();
            const errorMsg = error instanceof Error ? error.message : String(error);
            vscode.window.showErrorMessage(`加载开发板配置失败: ${errorMsg}`);
        }
    }

    async _listPorts(): Promise<string[]> {
        try {
            const ports = await SerialPort.list();
            this._logger.debug('扫描串口: ' + JSON.stringify(ports, null, 2));
            return ports.filter((portInfo: any) => {
                if (!portInfo?.path) return false;
                const path = portInfo.path.toLowerCase();
                return path.includes('usbserial') || path.includes('usbmodem') ||
                    path.includes('slab_usbtouart') || path.includes('ttyusb') ||
                    path.includes('ttyacm') || /^com\d+/.test(path);
            }).map((portInfo: any) => portInfo.path);
        } catch (error) {
            this._logger.warn(`串口扫描错误: ${error instanceof Error ? error.message : String(error)}`);
            return [];
        }
    }

    async selectPort(port?: string): Promise<string | undefined> {
        if (!port) {
            this._logger.debug('Scanning for available ports...');
            const ports = await this._listPorts();
            this._logger.debug(`Found ${ports.length} available ports: ${ports.join(', ')}`);

            if (ports.length === 0) {
                this._logger.warn('No available MPY device ports found');
                vscode.window.showWarningMessage('无可用的MPY设备串口');
                return undefined;
            }

            this._logger.debug('Showing port selection dialog...');
            const selection = await vscode.window.showQuickPick(ports, {
                placeHolder: '选择MPY设备串口',
                title: '选择串口设备'
            });

            if (!selection) {
                this._logger.debug('User cancelled port selection');
                return undefined;
            }

            this._logger.debug(`User selected port: ${selection}`);
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
            this._logger.debug('No port selected, attempting to select port...');
            const ports = await this.selectPort();
            port = this._currentPort;
            if (!port) {
                this._logger.debug('User cancelled port selection');
                throw new Error('未选择串口设备');
            }
        }
        
        // 如果已经连接到相同端口，直接返回
        if (this.isConnected() && this._currentPort === port) {
            this._logger.debug(`Already connected to ${port}, skipping connection`);
            return;
        }
        
        if (this._isConnecting) {
            this._logger.debug('Connection already in progress, waiting...');
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
            await vscode.commands.executeCommand('setContext', 'mpyStudio.deviceConnected', true);
            // 连接成功后自动刷新 TreeView
            this._deviceFolder?.refresh();
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
        
        // 如果已经连接，跳过重连
        if (this.isConnected() && this._currentPort === port) {
            this._logger.debug(`Already connected to ${port}, skipping reconnect`);
            return;
        }
        
        if (this._isConnecting) {
            this._logger.debug('Reconnection already in progress, waiting...');
            throw new Error('正在连接中...');
        }
        
        this._isConnecting = true;
        try {
            if (!this._board) {
                this._board = new MicroPythonBoard();
            }
            
            this._logger.debug(`Reconnecting to port ${port}...`);
            await this._board.open(port);
            this._replPanel?.setStatus?.(`已连接: ${port}`, true);
            
            if (this._dataListener) this._board.parser?.removeListener('data', this._dataListener);
            this._dataListener = (line: string) => {
                this._replPanel?.addOutput?.(line, 'output');
            };
            this._board.parser?.on('data', this._dataListener);
            this._board.serial?.on('close', () => this._handleSerialClosed());
            
            // 硬重启后的重连不需要握手验证，设备刚启动会自动发送启动信息
            this._currentPort = port;
            this._logger.info(`重连成功到端口 ${port}`);
            this._updateStatusBar();
            await vscode.commands.executeCommand('setContext', 'mpyStudio.deviceConnected', true);
            
            // 连接成功后刷新设备文件树
            this._deviceFolder?.refresh();
        } catch (error) {
            this._logger.warn(`重连失败: ${error instanceof Error ? error.message : String(error)}`);
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
        for (const [tmpFile, devicePath] of this.openFileMap.entries()) {
            const editors = vscode.window.visibleTextEditors.filter(e => e.document.fileName === tmpFile);
            for (const editor of editors) {
                await vscode.window.showTextDocument(editor.document, { preview: false, preserveFocus: false });
                await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
            }
            const doc = vscode.workspace.textDocuments.find(d => d.fileName === tmpFile);
            if (doc) {
                await vscode.window.showTextDocument(doc, { preview: false, preserveFocus: false });
                await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
            }
            try {
                require('fs').unlinkSync(tmpFile);
            } catch (e) {
            }
        }
        this.openFileMap.clear();
        if (this._board) {
            try {
                await this._board.close();
            } catch { }
            this._board = null;
        }
        this._currentPort = undefined;
        this._updateStatusBar();
        vscode.commands.executeCommand('setContext', 'mpyStudio.deviceConnected', false);
    }

    async getPrompt(): Promise<string> {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.get_prompt() as string;
    }

    async run(code: string): Promise<string> {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.run(code) as string;
    }

    async loadFile(filePath: string): Promise<string> {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.fs_cat(filePath);
    }

    async writeFile(filePath: string, content: string): Promise<void> {
        if (!this._board) throw new Error('设备未连接');
        await this._board.fs_put(content, filePath);
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

    async stop(): Promise<void> {
        if (!this._board) throw new Error('设备未连接');
        await this._board.stop();
        return Promise.resolve();
    }

    async forceStopWithTimerKill(): Promise<void> {
        if (!this._board) throw new Error('设备未连接');
        await this._board.forceStopWithTimerKill();
        return Promise.resolve();
    }

    async reset() {
        if (!this._board) throw new Error('设备未连接');
        await this._board?.stop();
        await this._board?.exit_raw_repl();
        await this._board?.reset();
        return Promise.resolve();
    }

    async fs_rm(filePath: string) {
        if (!this._board) throw new Error('设备未连接');
        return await this._board.fs_rm(filePath);
    }

    public async deleteFolder(fullPath: string, context: vscode.ExtensionContext) {
        if (!this._board) throw new Error('设备未连接');
        const helpersPath = path.join(context.extensionPath, 'media', 'helpers.py');
        await this._board.execfile(helpersPath);
        await this._board.run(`delete_folder('${fullPath}')`);
    }

    public async createFile(folderPath: string, fileName: string, context: vscode.ExtensionContext) {
        if (!this._board) throw new Error('设备未连接');
        const filePath = folderPath.endsWith('/') ? folderPath + fileName : folderPath + '/' + fileName;
        await this._board.run(`with open('${filePath}', 'w') as f: pass`);
    }

    public async createFolder(folderPath: string, folderName: string, context: vscode.ExtensionContext) {
        if (!this._board) throw new Error('设备未连接');
        const dirPath = folderPath.endsWith('/') ? folderPath + folderName : folderPath + '/' + folderName;
        await this._board.run(`import uos; uos.mkdir('${dirPath}')`);
    }

    public getDeviceFolder() {
        return this._deviceFolder;
    }

    setDeviceFolder(folder: DeviceFolder) {
        this._deviceFolder = folder;
    }

    getBoard(): MicroPythonBoard | null {
        return this._board;
    }

    dispose() {
        this._statusBarItem?.dispose();
        this._boardStatusBarItem?.dispose();
        this._board?.close();
    }

    getOpenFileMap() {
        return this.openFileMap;
    }
} 