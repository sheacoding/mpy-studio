import * as vscode from 'vscode';
import { SerialPort } from 'serialport';
import { PortInfo } from '@serialport/bindings-cpp';
import { ExtensionLogger } from './logger';

export class SerialDeviceManager {
    private statusBarItem: vscode.StatusBarItem;
    private lastSelectedPort: string | undefined;
    private logger: ExtensionLogger;

    constructor(logger: ExtensionLogger) {
        this.logger = logger;
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.statusBarItem.command = 'extension.micropythonSelectPort';
        this.updateStatusBar();
        this.statusBarItem.show();
    }

    private updateStatusBar() {
        if (this.lastSelectedPort) {
            this.statusBarItem.text = `$(plug) MicroPython (${this.lastSelectedPort})`;
            this.statusBarItem.tooltip = '点击选择串口设备';
        } else {
            this.statusBarItem.text = '$(circle-slash) MicroPython (未选择)';
            this.statusBarItem.tooltip = '点击选择串口设备';
        }
    }

    // 列出所有串口（用于状态栏）
    async listAllPorts(): Promise<string[]> {
        try {
            const ports = await SerialPort.list();
            return ports.map((portInfo: PortInfo) => portInfo.path);
        } catch (error) {
            this.logger.log(`SerialDeviceManager: Error listing all ports: ${error instanceof Error ? error.message : String(error)}`);
            throw error;
        }
    }

    // 列出可能的 MicroPython 设备串口（用于菜单选择）
    async listMicroPythonPorts(): Promise<string[]> {
        try {
            const ports = await SerialPort.list();
            return ports
                .filter((portInfo: PortInfo) => {
                    // 在 macOS 上，MicroPython 设备通常显示为 /dev/cu.usbserial-* 或 /dev/cu.SLAB_USBtoUART
                    // 在 Windows 上，通常是 COM* 端口
                    // 在 Linux 上，通常是 /dev/ttyUSB* 或 /dev/ttyACM*
                    const path = portInfo.path.toLowerCase();
                    return path.includes('usbserial') || 
                           path.includes('slab_usbtobart') ||
                           path.includes('ttyusb') || 
                           path.includes('ttyacm') ||
                           /^com\d+/.test(path);
                })
                .map((portInfo: PortInfo) => portInfo.path);
        } catch (error) {
            this.logger.log(`SerialDeviceManager: Error listing MicroPython ports: ${error instanceof Error ? error.message : String(error)}`);
            throw error;
        }
    }

    // 检查端口是否可用
    async checkPort(port: string): Promise<boolean> {
        try {
            // 尝试快速打开和关闭端口来检查其可用性
            const testPort = new SerialPort({
                path: port,
                baudRate: 115200,
                autoOpen: false
            });

            return new Promise((resolve) => {
                testPort.open((error) => {
                    if (error) {
                        resolve(false);
                        return;
                    }
                    testPort.close(() => resolve(true));
                });
            });
        } catch {
            return false;
        }
    }

    // 选择并记住端口
    async selectPort(port: string): Promise<void> {
        try {
            const isAvailable = await this.checkPort(port);
            if (!isAvailable) {
                throw new Error(`串口 ${port} 不可用`);
            }
            
            this.lastSelectedPort = port;
            this.updateStatusBar();
            this.logger.log(`SerialDeviceManager: Selected port ${port}`);
        } catch (error) {
            this.logger.log(`SerialDeviceManager: Error selecting port: ${error instanceof Error ? error.message : String(error)}`);
            throw error;
        }
    }

    // 清除选择的端口
    clearPort() {
        this.lastSelectedPort = undefined;
        this.updateStatusBar();
        this.logger.log('SerialDeviceManager: Cleared port selection');
    }

    hasSelectedPort(): boolean {
        return !!this.lastSelectedPort;
    }

    getCurrentPort(): string | undefined {
        return this.lastSelectedPort;
    }

    dispose() {
        this.logger.log('SerialDeviceManager: Disposing...');
        this.statusBarItem.dispose();
    }
}