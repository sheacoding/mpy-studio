import * as vscode from 'vscode';
// @ts-ignore
import { DeviceManager } from './board';
import { Runner } from './runner';
import { Logger } from './logger';
import { ReplPanel } from './repl-panel';
import * as path from 'path';

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
    try {
        vscode.window.showInformationMessage('mpy-studio 扩展已激活！');
        
        let logger: Logger;
        
        try {
            outputChannel = vscode.window.createOutputChannel('MPY-REPL');
            logger = Logger.getInstance(context, outputChannel);

            deviceManager = new DeviceManager(logger, undefined, context);
            replPanel = new ReplPanel(context, deviceManager);
            (deviceManager as any)._replPanel = replPanel;
            runner = new Runner(logger, deviceManager);
            await deviceManager.loadConfig(context);

        } catch (initError) {
            outputChannel = vscode.window.createOutputChannel('MPY-REPL');
            logger = Logger.getInstance(context, outputChannel);
        }

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
                    if (replPanel) {
                        replPanel.addOutput('请先打开一个Python文件', 'error');
                    } else {
                        showMessage('请先打开一个Python文件', 'error');
                    }
                    return;
                }
                const fileName = editor.document.fileName.toLowerCase();
                const languageId = editor.document.languageId.toLowerCase();
                const isPythonFile = fileName.endsWith('.py') || languageId === 'python';
                if (!isPythonFile) {
                    if (replPanel) {
                        replPanel.addOutput('只能运行 Python 文件', 'error');
                    } else {
                        showMessage('只能运行 Python 文件', 'error');
                    }
                    return;
                }
                if (editor.document.isDirty) {
                    await editor.document.save();
                }
                
                try {
                    await vscode.commands.executeCommand('mpy-studio.replPanel.focus');
                    
                } catch (focusError) {
                }
                
                try {
                    const filePath = editor.document.uri.fsPath;
                    if (!filePath) {
                        if (replPanel) {
                            replPanel.addOutput('无法获取当前文件路径', 'error');
                        } else {
                            showMessage('无法获取当前文件路径', 'error');
                        }
                        return;
                    }
                    
                    if (!runner) {
                        showMessage('运行器未初始化，无法运行文件', 'error');
                        return;
                    }
                    
                    if (replPanel) {
                        replPanel.addOutput(`运行文件: ${filePath}`, 'info');
                    }
                    const success = await runner.runFile(filePath);
                } catch (err) {
                    const errorMessage = err instanceof Error ? err.message : String(err);
                    if (errorMessage == 'pre stop') {
                        return;
                    }
                    return;
                }
            }),

            vscode.commands.registerCommand('extension.mpyStop', async () => {
                try {
                    if (!runner) {
                        showMessage('运行器未初始化，无法停止运行', 'error');
                        return;
                    }
                    await runner.stop();
                } catch (err) {
                }
            }),

            vscode.commands.registerCommand('extension.mpyMAIN', async () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法上传文件', 'error');
                        return;
                    }

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

                    try {
                        await vscode.commands.executeCommand('mpy-studio.replPanel.focus');
                        
                    } catch (focusError) {
                    }

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

                    if (replPanel) {
                        replPanel.addOutput(`已上传 ${fileName} 到设备 main.py`, 'info');
                    }
                    
                    showMessage(`已上传 ${fileName} 到设备 main.py`);
                } catch (err) {
                    const errorMessage = err instanceof Error ? err.message : String(err);
                    
                    if (replPanel) {
                        replPanel.addOutput(`上传失败: ${errorMessage}`, 'error');
                    }
                    
                    showMessage('上传失败: ' + errorMessage, 'error');
                }
            }),

            vscode.commands.registerCommand('extension.mpyHardReset', async () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法重启设备', 'error');
                        return;
                    }
                    
                    try {
                        await deviceManager.connect();
                    } catch (connErr) {
                        const msg = connErr instanceof Error ? connErr.message : String(connErr);
                        showMessage('设备连接失败: ' + msg, 'error');
                        return;
                    }
                    
                    await deviceManager.hard_reset();
                    
                    if (replPanel) {
                        replPanel.addOutput('硬重启完成', 'info');
                    }
                    
                    showMessage('硬重启完成');
                } catch (err) {
                    const errorMessage = err instanceof Error ? err.message : String(err);
                    
                    if (replPanel) {
                        replPanel.addOutput(`硬重启失败: ${errorMessage}`, 'error');
                    }
                    
                    showMessage('硬重启失败: ' + errorMessage, 'error');
                }
            }),

            vscode.commands.registerCommand('extension.mpySelectPort', async () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法选择端口', 'error');
                        return;
                    }
                    
                    await deviceManager.selectPort();
                } catch (err) {
                    showMessage('选择端口失败: ' + (err instanceof Error ? err.message : String(err)), 'error');
                }
            }),

            vscode.commands.registerCommand('extension.mpyDisconnect', () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法断开连接', 'error');
                        return;
                    }
                    
                    deviceManager.disconnect();
                } catch (err) {
                }
            }),

            vscode.commands.registerCommand('extension.mpyClear', async () => {
                if (!deviceManager) {
                    showMessage('设备管理器未初始化，无法清除主程序', 'error');
                    return;
                }
                
                let port = deviceManager.getCurrentPort();
                if (!port) {
                    showMessage('未选择设备，无法清除主程序', 'warning');
                    return;
                }
                
                try {
                    if (!runner) {
                        showMessage('运行器未初始化，无法清除主程序', 'error');
                        return;
                    }
                    
                    await runner.clearMainPy();
                    
                    if (outputChannel) {
                        outputChannel.clear();
                    }
                    
                    showMessage('已清除设备 main.py 并清空输出');
                } catch (err) {
                    showMessage('清除失败: ' + (err instanceof Error ? err.message : String(err)), 'error');
                }
            }),

            vscode.commands.registerCommand('extension.mpyShowLogs', () => {
                outputChannel.show();
            }),

            vscode.commands.registerCommand('extension.mpyREPL', async () => {
                if (!replPanel) {
                    showMessage('REPL面板未初始化，无法显示', 'error');
                    return;
                }
                
                if ((replPanel as any)._view) {
                    (replPanel as any)._view?.show?.(true);
                } else {
                    try {
                        await vscode.commands.executeCommand('mpy-studio.replPanel.focus');
                        
                        setTimeout(() => {
                            if ((replPanel as any)._view) {
                                showMessage('REPL 面板已打开', 'info');
                            } else {
                                showMessage('请手动打开 MPY-REPL 面板', 'warning');
                            }
                        }, 1000);
                        
                    } catch (focusError) {
                        showMessage('请手动打开 MPY-REPL 面板', 'warning');
                    }
                }
            }),

            vscode.commands.registerCommand('extension.mpyStatusBarConnect', async () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法连接设备', 'error');
                        return;
                    }
                    
                    await deviceManager.connect();
                } catch (err) {
                    showMessage('连接设备失败: ' + (err instanceof Error ? err.message : String(err)), 'error');
                }
            }),

            vscode.commands.registerCommand('extension.selectBoard', async () => {
                try {
                    if (!deviceManager) {
                        showMessage('设备管理器未初始化，无法选择开发板', 'error');
                        return;
                    }
                    
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

        context.subscriptions.push(...commands, outputChannel);
        
        if (replPanel) {
            context.subscriptions.push(
                vscode.window.registerWebviewViewProvider(
                    ReplPanel.viewType,
                    replPanel
                )
            );
        }
    } catch (error) {
        vscode.window.showErrorMessage(`mpy-studio扩展激活失败: ${error instanceof Error ? error.message : String(error)}`);
    }
}

export function deactivate() {
    if (deviceManager) {
        deviceManager.dispose();
    }
}