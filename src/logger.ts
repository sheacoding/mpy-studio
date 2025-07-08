import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3
}

export class Logger {
    private static instance: Logger;
    private logFile: string;
    private outputChannel: vscode.OutputChannel;
    private currentLevel: LogLevel = LogLevel.DEBUG;

    private constructor(context: vscode.ExtensionContext, outputChannel?: vscode.OutputChannel) {
        const logDir = context.globalStorageUri.fsPath;
        this.logFile = path.join(logDir, 'micropython.log');
        this.outputChannel = outputChannel || vscode.window.createOutputChannel('MPY-REPL');

        // 确保日志目录存在
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 清空或创建日志文件
        fs.writeFileSync(this.logFile, '');
    }

    public static getInstance(context?: vscode.ExtensionContext, outputChannel?: vscode.OutputChannel): Logger {
        if (!Logger.instance && context) {
            Logger.instance = new Logger(context, outputChannel);
        }
        return Logger.instance;
    }

    public setLevel(level: LogLevel): void {
        this.currentLevel = level;
    }

    private shouldLog(level: LogLevel): boolean {
        return level >= this.currentLevel;
    }

    private formatMessage(level: LogLevel, message: string): string {
        const timestamp = new Date().toISOString();
        const levelName = LogLevel[level];
        return `[${timestamp}] [${levelName}] ${message}`;
    }

    public debug(message: string, showInOutputChannel: boolean = false): void {
        if (this.shouldLog(LogLevel.DEBUG)) {
            const logMessage = this.formatMessage(LogLevel.DEBUG, message);
            this.writeLog(logMessage, showInOutputChannel);
        }
    }

    public info(message: string, showInOutputChannel: boolean = true): void {
        if (this.shouldLog(LogLevel.INFO)) {
            const logMessage = this.formatMessage(LogLevel.INFO, message);
            this.writeLog(logMessage, showInOutputChannel);
        }
    }

    public warn(message: string, showInOutputChannel: boolean = true): void {
        if (this.shouldLog(LogLevel.WARN)) {
            const logMessage = this.formatMessage(LogLevel.WARN, message);
            this.writeLog(logMessage, showInOutputChannel);
        }
    }

    public error(message: string, showInOutputChannel: boolean = true): void {
        if (this.shouldLog(LogLevel.ERROR)) {
            const logMessage = this.formatMessage(LogLevel.ERROR, message);
            this.writeLog(logMessage, showInOutputChannel);
        }
    }

    private writeLog(logMessage: string, showInOutputChannel: boolean): void {
        // 写入日志文件
        fs.appendFileSync(this.logFile, logMessage + '\n');

        // 可选地显示在输出通道
        if (showInOutputChannel) {
            this.outputChannel.appendLine(logMessage);
        }
    }

    public showLog(): void {
        this.outputChannel.show();
    }
}