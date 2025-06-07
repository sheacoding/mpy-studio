import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export class ExtensionLogger {
    private static instance: ExtensionLogger;
    private logFile: string;
    private outputChannel: vscode.OutputChannel;

    private constructor(context: vscode.ExtensionContext, outputChannel?: vscode.OutputChannel) {
        const logDir = context.globalStorageUri.fsPath;
        this.logFile = path.join(logDir, 'micropython-extension.log');
        this.outputChannel = outputChannel || vscode.window.createOutputChannel('MicroPython Extension');

        // 确保日志目录存在
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 清空或创建日志文件
        fs.writeFileSync(this.logFile, '');
    }

    public static getInstance(context?: vscode.ExtensionContext, outputChannel?: vscode.OutputChannel): ExtensionLogger {
        if (!ExtensionLogger.instance && context) {
            ExtensionLogger.instance = new ExtensionLogger(context, outputChannel);
        }
        return ExtensionLogger.instance;
    }

    public log(message: string, showInOutputChannel: boolean = true) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${message}\n`;

        // 写入日志文件
        fs.appendFileSync(this.logFile, logMessage);

        // 可选地显示在输出通道
        if (showInOutputChannel) {
            this.outputChannel.appendLine(logMessage.trim());
        }
    }

    public showLog() {
        this.outputChannel.show();
    }

    public getLogFilePath(): string {
        return this.logFile;
    }
}