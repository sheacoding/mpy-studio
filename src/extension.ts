import * as vscode from 'vscode';
// @ts-ignore
import { DeviceManager } from './board';
import { Runner } from './runner';
import { Logger } from './logger';
import { ReplPanel } from './repl-panel';
import * as path from 'path';
import * as fs from 'fs';

let outputChannel: vscode.OutputChannel;
let deviceManager: DeviceManager;
let runner: Runner;
let replPanel: ReplPanel;

// 显示消息的辅助函数
function showMessage(message: string, type: 'info' | 'warning' | 'error' = 'info'): void {
    switch (type) {
        case 'info':
            vscode.window.showInformationMessage(message);
            break;
        case 'warning':
            vscode.window.showWarningMessage(message);
            break;
        case 'error':
            vscode.window.showErrorMessage(message);
            break;
    }
}

// 更新类型定义
async function updateTypings(context: vscode.ExtensionContext) {
    const pythonConfig = vscode.workspace.getConfiguration('python.analysis');
    const typingsPath = path.join(context.extensionPath, 'out', 'typings');

    pythonConfig.update('typeCheckingMode', 'basic', vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('stubPath', path.join(typingsPath, 'esp32'), vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('typeshedPaths', [path.join(typingsPath, 'esp32')], vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('extraPaths', [path.join(typingsPath, 'mpbit')], vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('diagnosticSeverityOverrides', {
        'reportMissingModuleSource': 'none',
    }, vscode.ConfigurationTarget.Workspace);
}

export async function activate(context: vscode.ExtensionContext) {
    console.log('MPY Studio: Extension activating...');
    
    outputChannel = vscode.window.createOutputChannel('MPY-REPL');
    const logger = Logger.getInstance(context, outputChannel);

    // 初始化管理器

    // typings 目录已保证存在，下面再初始化依赖配置的对象
    deviceManager = new DeviceManager(logger, undefined, context);
    replPanel = new ReplPanel(context, deviceManager);
    (deviceManager as any)._replPanel = replPanel;
    runner = new Runner(logger, deviceManager, replPanel);
    await deviceManager.loadConfig(context);

    console.log('MPY Studio: Managers initialized, registering commands...');

    // 注册命令
    const commands = [
        vscode.commands.registerCommand('extension.updateTypings', async () => {
            try {
                // 重新加载配置以更新类型定义
                await deviceManager.loadConfig(context);
                showMessage('MicroPython 类型定义已更新');
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                showMessage(`更新类型定义失败: ${errorMsg}`, 'error');
            }
        }),

        vscode.commands.registerCommand('extension.mpyMenu', () => {
            showMessage('请选择上方按钮下拉菜单中的操作');
        }),

        vscode.commands.registerCommand('extension.mpyRUN', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                replPanel.addOutput('请先打开一个Python文件', 'error');
                return;
            }
            const fileName = editor.document.fileName.toLowerCase();
            const languageId = editor.document.languageId.toLowerCase();
            const isPythonFile = fileName.endsWith('.py') || languageId === 'python';
            if (!isPythonFile) {
                replPanel.addOutput('只能运行 Python 文件', 'error');
                return;
            }
            if (editor.document.isDirty) {
                await editor.document.save();
            }
            try {
                const filePath = editor.document.uri.fsPath;
                if (!filePath) {
                    replPanel.addOutput('无法获取当前文件路径', 'error');
                    return;
                }
                replPanel.addOutput(`运行文件: ${filePath}`, 'info');
                const success = await runner.runFile(filePath);
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : String(err);
                if (errorMessage == 'pre stop') {
                    return;
                }
                logger.warn('运行文件失败:' + errorMessage);
                return;
            }
        }),

        vscode.commands.registerCommand('extension.mpyStop', async () => {
            try {
                await runner.stop();
            } catch (err) {
            }
        }),

        vscode.commands.registerCommand('extension.mpyMAIN', async () => {
            try {
                const editor = vscode.window.activeTextEditor;
                if (!editor) {
                    showMessage('请先打开一个 Python 文件', 'warning');
                    return;
                }

                const filePath = editor.document.uri.fsPath;
                if (!filePath) {
                    showMessage('无法获取当前文件路径', 'error');
                    return;
                }
                const fileName = path.basename(filePath);

                // 连接串口，自动处理端口选择
                try {
                    await deviceManager.connect();
                } catch (connErr) {
                    return;
                }

                await vscode.window.withProgress({
                    location: vscode.ProgressLocation.Notification,
                    title: `正在上传 ${fileName} 到设备 main.py`,
                    cancellable: false
                }, async (progress) => {
                    await deviceManager.fs_put(filePath, 'main.py', (msg) => {
                        progress.report({ increment: parseInt(msg) });
                    });
                });

                replPanel.addOutput(`已上传 ${fileName} 到设备 main.py`, 'info');
                logger.info(`上传文件: ${fileName} 到 main.py`);
                showMessage(`已上传 ${fileName} 到设备 main.py`);
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : String(err);
                logger.error('上传文件失败: ' + errorMessage);
                replPanel.addOutput(`上传失败: ${errorMessage}`, 'error');
                showMessage('上传失败: ' + errorMessage, 'error');
            }
        }),

        vscode.commands.registerCommand('extension.mpyHardReset', async () => {
            try {
                try {
                    await deviceManager.connect();
                } catch (connErr) {
                    const msg = connErr instanceof Error ? connErr.message : String(connErr);
                    logger.error('设备连接失败: ' + msg);
                    showMessage('设备连接失败: ' + msg, 'error');
                    return;
                }
                await deviceManager.hard_reset();
                replPanel.addOutput('硬重启完成', 'info');
                showMessage('硬重启完成');
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : String(err);
                logger.error('硬重启失败: ' + errorMessage);
                replPanel.addOutput(`硬重启失败: ${errorMessage}`, 'error');
                showMessage('硬重启失败: ' + errorMessage, 'error');
            }
        }),

        vscode.commands.registerCommand('extension.mpySelectPort', async () => {
            await deviceManager.selectPort();
        }),

        vscode.commands.registerCommand('extension.mpyDisconnect', () => {
            try {
                deviceManager.disconnect();
            } catch (err) {
            }
        }),

        vscode.commands.registerCommand('extension.mpyClear', async () => {
            let port = deviceManager.getCurrentPort();
            if (!port) {
                showMessage('未选择设备，无法清除主程序', 'warning');
                return;
            }
            try {
                await runner.clearMainPy();
                outputChannel.clear();
                showMessage('已清除设备 main.py 并清空输出');
            } catch (err) {
                showMessage('清除失败: ' + (err instanceof Error ? err.message : String(err)), 'error');
            }
        }),

        vscode.commands.registerCommand('extension.mpyShowLogs', () => {
            outputChannel.show();
        }),

        vscode.commands.registerCommand('extension.mpyREPL', async () => {
            if ((replPanel as any)._view) {
                (replPanel as any)._view?.show?.(true);
            }
        }),

        vscode.commands.registerCommand('extension.mpyStatusBarConnect', async () => {
            try {
                await deviceManager.connect();
            } catch (err) {
                showMessage('连接设备失败: ' + (err instanceof Error ? err.message : String(err)), 'error');
            }
        }),

        vscode.commands.registerCommand('extension.selectBoard', async () => {
            try {
                // 获取可用的开发板列表
                const config = await deviceManager.getStubsManager().loadConfig();

                if (!config.boards || Object.keys(config.boards).length === 0) {
                    showMessage('配置文件中没有可用的开发板', 'error');
                    return;
                }

                // 显示开发板选择列表
                const boardEntries = Object.entries(config.boards).map(([key, board]) => ({
                    label: `${(board as any).name || key} (${(board as any).board || ''})`,
                    key: key
                }));

                // 添加 PYTHON 选项到列表开头
                const allOptions = [
                    {
                        label: 'PYTHON (系统)',
                        key: 'python'
                    },
                    ...boardEntries
                ];

                const selection = await vscode.window.showQuickPick(allOptions, {
                    placeHolder: '选择开发板',
                    title: '选择开发板'
                });

                if (selection) {
                    const selectedBoardKey = (selection as any).key;

                    // 更新 Python 分析配置
                    const boardConfig = config.boards?.[selectedBoardKey];
                    await deviceManager.getStubsManager().updateSettingsForBoard(selectedBoardKey, boardConfig);

                    // 重新加载配置
                    await deviceManager.loadConfig(context);
                }
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                showMessage(`选择开发板失败: ${errorMsg}`, 'error');
            }
        }),
    ];

    // 注册所有命令
    context.subscriptions.push(...commands, outputChannel,
        vscode.window.registerWebviewViewProvider(
            ReplPanel.viewType,
            replPanel
        )
    );
    
    console.log('MPY Studio: Extension activated successfully. Registered commands:', commands.length);
}

export function deactivate() {
    if (deviceManager) {
        deviceManager.dispose();
    }
}