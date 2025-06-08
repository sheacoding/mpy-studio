import * as vscode from 'vscode';
import { SerialPort } from 'serialport';
import { ExtensionLogger } from './logger';
import { SerialDeviceManager } from './serialManager';
import * as path from 'path';

let serialPort: SerialPort | undefined;
let outputChannel: vscode.OutputChannel;
let serialManager: SerialDeviceManager;

export function activate(context: vscode.ExtensionContext) {
    // 使用统一的输出通道名称
    outputChannel = vscode.window.createOutputChannel('MicroPython Extension');
    const logger = ExtensionLogger.getInstance(context, outputChannel);
    
    // 配置 Python 分析器设置
    const pythonConfig = vscode.workspace.getConfiguration('python.analysis');
    
    // 1. 配置 extraPaths
    const currentExtraPaths = pythonConfig.get<string[]>('extraPaths') || [];
    const typingsBasePath = path.join(context.extensionPath, 'out', 'typings');
    const typingsPaths = [
        path.join(typingsBasePath, 'stdlib'),
        path.join(typingsBasePath, 'mpbit')
    ];
    
    // 检查并添加新路径
    const pathsToAdd = typingsPaths.filter(p => !currentExtraPaths.includes(p));
    if (pathsToAdd.length > 0) {
        const newPaths = [...currentExtraPaths, ...pathsToAdd];
        pythonConfig.update('extraPaths', newPaths, vscode.ConfigurationTarget.Workspace);
        logger.log(`添加了 ${pathsToAdd.length} 个新的类型定义路径`);
    }

    // 2. 配置其他 Python 分析器设置
    pythonConfig.update('typeCheckingMode', 'off', vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('diagnosticMode', 'workspace', vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('stubPath', path.join(context.extensionPath, 'out', 'typings/esp32'), vscode.ConfigurationTarget.Workspace);
    
    // 3. 配置诊断设置，禁用标准库相关检查
    pythonConfig.update('diagnosticSeverityOverrides', {
        'reportMissingModuleSource': 'none',
        'reportMissingImports': 'none',
        'reportMissingStandardImports': 'none',
        'reportImportCycles': 'none',
        'reportUndefinedVariable': 'warning'  // 只对未定义变量发出警告
    }, vscode.ConfigurationTarget.Workspace);

    logger.log('已配置 Python 分析器设置');

    // 初始化 serialManager
    serialManager = new SerialDeviceManager(logger);

    // 注册 micropythonMenu 命令
    // 由于菜单已通过 package.json 的 submenu 机制实现，无需再弹出 QuickPick
    // 可保留命令注册用于命令面板或其它用途
    let micropythonMenu = vscode.commands.registerCommand('extension.micropythonMenu', async (e: any) => {
        vscode.window.showInformationMessage('请选择上方按钮下拉菜单中的操作');
    });

    // 注册其他命令
    let runCommand = vscode.commands.registerCommand('extension.micropythonRUN', async () => {
        // 获取当前激活的文本编辑器
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个 Python 文件');
            return;
        }

        // 检查是否为 Python 文件
        if (editor.document.languageId !== 'python') {
            vscode.window.showWarningMessage('只能运行 Python 文件');
            return;
        }

        // 确保文件已保存
        if (editor.document.isDirty) {
            await editor.document.save();
        }

        try {
            // 检查是否有 REPL 终端在运行
            const terminals = vscode.window.terminals;
            const replTerminal = terminals.find(t => t.name === 'MicroPython REPL');
            if (replTerminal) {
                const proceed = await vscode.window.showWarningMessage(
                    'REPL 正在运行，需要先关闭它才能运行文件。是否关闭 REPL？',
                    '关闭',
                    '取消'
                );
                if (proceed === '关闭') {
                    replTerminal.dispose();
                    // 等待终端完全关闭
                    await new Promise(resolve => setTimeout(resolve, 1000));
                } else {
                    return;
                }
            }

            // 获取当前端口
            let port = serialManager.getCurrentPort();
            
            // 如果没有选择端口，提示选择
            if (!port) {
                const connect = await vscode.window.showWarningMessage(
                    '未选择设备，是否选择串口？',
                    '选择',
                    '取消'
                );
                if (connect === '选择') {
                    await vscode.commands.executeCommand('extension.micropythonSelectPort');
                    // 重新获取端口
                    port = serialManager.getCurrentPort();
                    if (!port) {
                        throw new Error('未选择串口设备');
                    }
                } else {
                    return;
                }
            }

            // 检查端口是否可用
            const isAvailable = await serialManager.checkPort(port);
            if (!isAvailable) {
                throw new Error(`串口 ${port} 不可用，请重新选择`);
            }

            // 获取文件路径并运行
            const filePath = editor.document.uri.fsPath;
            
            outputChannel.show();
            outputChannel.clear();
            outputChannel.appendLine(`正在运行文件...`);
            
            // 使用 mpremote 运行文件
            await new Promise<void>((resolve, reject) => {
                const cmd = `mpremote connect ${port} run "${filePath}"`;
                outputChannel.appendLine(`执行命令: ${cmd}`);
                
                const process = require('child_process').exec(cmd, (error: Error | null, stdout: string, stderr: string) => {
                    if (error) {
                        reject(new Error(stderr || error.message));
                        return;
                    }
                    if (stdout) outputChannel.appendLine(stdout);
                    if (stderr) outputChannel.appendLine(stderr);
                    resolve();
                });
                
                // 设置超时检测
                setTimeout(() => {
                    process.kill();
                    reject(new Error('运行超时，请检查程序是否正确'));
                }, 10000); // 10秒超时
            });

            outputChannel.appendLine('运行完成');

        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            vscode.window.showErrorMessage(`运行错误: ${message}`);
            outputChannel.appendLine(`错误: ${message}`);
        }
    });

    let replCommand = vscode.commands.registerCommand('extension.micropythonREPL', async () => {
        try {
            // 检查是否已选择串口
            if (!serialManager.hasSelectedPort()) {
                const connect = await vscode.window.showWarningMessage(
                    '未选择设备，是否选择串口？',
                    '选择',
                    '取消'
                );
                if (connect === '选择') {
                    await vscode.commands.executeCommand('extension.micropythonSelectPort');
                } else {
                    return;
                }
            }

            // 获取当前串口
            const port = serialManager.getCurrentPort();
            if (!port) {
                vscode.window.showErrorMessage('未选择串口设备');
                return;
            }

            // 检查端口是否可用
            const isAvailable = await serialManager.checkPort(port);
            if (!isAvailable) {
                throw new Error(`串口 ${port} 不可用，请重新选择`);
            }

            // 创建终端并运行 REPL
            const terminal = vscode.window.createTerminal('MicroPython REPL');
            terminal.show();

            // 在 macOS 和 Linux 上使用 stty 命令设置终端为原始模式
            if (process.platform !== 'win32') {
                terminal.sendText('stty raw -echo');
            }

            // 运行 mpremote repl，先执行 soft-reset 再进入 repl
            const cmd = `mpremote connect ${port} soft-reset repl`;
            terminal.sendText(cmd);

            // 注册终端关闭事件，重置终端设置
            const disposable = vscode.window.onDidCloseTerminal(async (closedTerminal) => {
                if (closedTerminal === terminal) {
                    // 重置终端设置（仅在非 Windows 系统上）
                    if (process.platform !== 'win32') {
                        const resetTerminal = vscode.window.createTerminal('Reset Terminal');
                        resetTerminal.sendText('stty sane');
                        setTimeout(() => resetTerminal.dispose(), 1000);
                    }
                    disposable.dispose();
                }
            });

        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            vscode.window.showErrorMessage(`打开 REPL 失败: ${message}`);
        }
    });

    let sendCommand = vscode.commands.registerCommand('extension.micropythonSEND', () => {
        vscode.window.showInformationMessage('上传当前文件');
    });

    let clearCommand = vscode.commands.registerCommand('extension.micropythonClear', async () => {
        try {
            // 检查是否已选择串口
            if (!serialManager.hasSelectedPort()) {
                const connect = await vscode.window.showWarningMessage(
                    '未选择设备，是否选择串口？',
                    '选择',
                    '取消'
                );
                if (connect === '选择') {
                    await vscode.commands.executeCommand('extension.micropythonSelectPort');
                } else {
                    return;
                }
            }

            // 获取当前串口
            const port = serialManager.getCurrentPort();
            if (!port) {
                vscode.window.showErrorMessage('未选择串口设备');
                return;
            }

            // 检查端口是否可用
            const isAvailable = await serialManager.checkPort(port);
            if (!isAvailable) {
                throw new Error(`串口 ${port} 不可用，请重新选择`);
            }

            // 确认是否清除程序
            const confirm = await vscode.window.showWarningMessage(
                '此操作将清除设备上的 main.py 程序，是否继续？',
                '确定',
                '取消'
            );
            
            if (confirm !== '确定') {
                return;
            }

            // 创建临时空文件并上传
            const fs = require('fs');
            const tempDir = path.join(context.extensionPath, 'temp');
            const emptyMainPath = path.join(tempDir, 'main.py');
            
            // 确保临时目录存在
            if (!fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir);
            }
            
            // 创建空的 main.py
            fs.writeFileSync(emptyMainPath, '');

            outputChannel.show();
            outputChannel.clear();
            outputChannel.appendLine('正在清除设备程序...');

            // 使用 mpremote 上传空文件
            await new Promise<void>((resolve, reject) => {
                const cmd = `mpremote connect ${port} cp "${emptyMainPath}" :main.py`;
                outputChannel.appendLine(`执行命令: ${cmd}`);
                
                const process = require('child_process').exec(cmd, (error: Error | null, stdout: string, stderr: string) => {
                    // 清理临时文件
                    fs.unlinkSync(emptyMainPath);
                    
                    if (error) {
                        reject(new Error(stderr || error.message));
                        return;
                    }
                    if (stdout) outputChannel.appendLine(stdout);
                    if (stderr) outputChannel.appendLine(stderr);
                    resolve();
                });
                
                // 设置超时
                setTimeout(() => {
                    process.kill();
                    fs.unlinkSync(emptyMainPath);
                    reject(new Error('操作超时，请重试'));
                }, 10000);
            });

            outputChannel.appendLine('设备程序已清除');
            vscode.window.showInformationMessage('设备程序已清除');

        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            vscode.window.showErrorMessage(`清除程序失败: ${message}`);
            outputChannel.appendLine(`错误: ${message}`);
        }
    });

    let disconnectCommand = vscode.commands.registerCommand('extension.micropythonDisconnect', async () => {
        try {
            if (!serialManager.hasSelectedPort()) {
                vscode.window.showInformationMessage('当前未选择任何设备');
                return;
            }
            
            // 清除选择的端口
            serialManager.clearPort();
            vscode.window.showInformationMessage('已清除设备选择');
        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            vscode.window.showErrorMessage(`操作失败: ${message}`);
        }
    });

    interface SerialPortInfo {
        path: string;
        manufacturer?: string;
        pid?: string;
        vid?: string;
    }

    let selectPortCommand = vscode.commands.registerCommand('extension.micropythonSelectPort', async () => {
        try {
            // 使用过滤后的 MicroPython 设备列表
            const ports = await serialManager.listMicroPythonPorts();
            if (ports.length === 0) {
                vscode.window.showWarningMessage('未检测到 MicroPython 设备');
                return;
            }

            // 创建选择项
            const items = ports.map(portPath => ({
                label: portPath,
                description: 'MicroPython 设备'
            }));

            // 显示串口选择菜单
            const selection = await vscode.window.showQuickPick(items, {
                placeHolder: '请选择 MicroPython 设备连接的串口'
            });

            if (!selection) return;

            // 选择并检查串口
            await serialManager.selectPort(selection.label);
        } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            vscode.window.showErrorMessage(`串口选择错误: ${message}`);
        }
    });

    let showLogsCommand = vscode.commands.registerCommand('extension.micropythonShowLogs', () => {
        outputChannel.show();
    });

    // 将所有命令添加到订阅列表
    context.subscriptions.push(
        micropythonMenu,
        runCommand,
        replCommand,
        sendCommand,
        selectPortCommand,
        disconnectCommand,
        clearCommand,
        showLogsCommand,
        outputChannel
    );
}

export function deactivate() {
    if (serialManager) {
        serialManager.dispose();
    }
}