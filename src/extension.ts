import * as vscode from 'vscode';
import { DeviceManager } from './board';
import { Runner } from './runner';
import { Logger } from './logger';
import { ReplPanel } from './repl-panel';
import { DeviceFolder } from './deviceFloder';
import * as fs from 'fs';
import * as nodePath from 'path';
// 临时文件与设备路径映射
// const openFileMap = new Map();

let deviceManager: DeviceManager | undefined;

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
    const typingsPath = nodePath.join(context.extensionPath, 'out', 'typings');

    pythonConfig.update('typeCheckingMode', 'basic', vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('stubPath', nodePath.join(typingsPath, 'esp32'), vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('typeshedPaths', [nodePath.join(typingsPath, 'esp32')], vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('extraPaths', [nodePath.join(typingsPath, 'mpbit')], vscode.ConfigurationTarget.Workspace);
    pythonConfig.update('diagnosticSeverityOverrides', {
        'reportMissingModuleSource': 'none',
    }, vscode.ConfigurationTarget.Workspace);
}

function devicePathToTmpFileName(devicePath: string) {
  // 替换所有 / 为 全角／，确保是单一文件名
  return devicePath.replace(/\//g, '／');
}

class DeviceTextDocumentContentProvider implements vscode.TextDocumentContentProvider {
  constructor(private deviceManager: any) {}
  async provideTextDocumentContent(uri: vscode.Uri): Promise<string> {
    // uri.path 就是设备文件路径
    return await this.deviceManager.loadFile(uri.path);
  }
}

export async function activate(context: vscode.ExtensionContext) {
    // 1. 变量声明（作用域提升，便于后续 deactivate 使用）
    const outputChannel = vscode.window.createOutputChannel('MPY-REPL');
    const logger = Logger.getInstance(context, outputChannel);
    // 先初始化 deviceManager
    deviceManager = new DeviceManager(logger, undefined, context);
    // 再初始化 DeviceFolder
    const deviceFolder = new DeviceFolder(deviceManager!, context, logger);
    vscode.window.createTreeView('mpy-studio.deviceFs', {
      treeDataProvider: deviceFolder
    });
    // 恢复 TreeView 相关命令注册
    context.subscriptions.push(
      vscode.commands.registerCommand('mpy-studio.refresh', (node?: any) => deviceFolder.refresh(node)),
      vscode.commands.registerCommand('mpy-studio.openFile', async (node: any) => {
        const ext = nodePath.extname(node.fullPath).toLowerCase();
        const imageExts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif'];
        const tmpRoot = nodePath.join(require('os').tmpdir(), 'mpy-device-tmp');
        const tmpFile = nodePath.join(tmpRoot, devicePathToTmpFileName(node.fullPath)); // 单一文件名
        // 不再需要 mkdirSync，因为不会有多级目录
        if (imageExts.includes(ext)) {
          // 读取二进制内容
          const bytes = await deviceManager!.getBoard()!.fs_cat_binary(node.fullPath);
          if (!bytes) {
            vscode.window.showErrorMessage('图片读取失败');
            return;
          }
          const arr = (typeof bytes === 'string' ? bytes : String(bytes)).split(',').filter(Boolean).map(Number);
          const buf = Buffer.from(arr);
          fs.writeFileSync(tmpFile, buf);
          const uri = vscode.Uri.file(tmpFile);
          vscode.commands.executeCommand('vscode.open', uri);
          return;
        }
        // 支持编辑的文本文件类型
        const editable = ['.py', '.txt', '.json', '.md', '.csv'];
        if (editable.includes(ext)) {
          // 从设备读取内容
          const content = await deviceManager!.loadFile(node.fullPath);
          fs.writeFileSync(tmpFile, content, 'utf8');
          deviceManager!.getOpenFileMap().set(tmpFile, node.fullPath);
          const doc = await vscode.workspace.openTextDocument(tmpFile);
          vscode.window.showTextDocument(doc, { preview: false });
        } else {
          // 其它文件（如二进制）仍用 provider 只读打开
          const uri = vscode.Uri.parse(`mpy-device:${node.fullPath}`);
          const doc = await vscode.workspace.openTextDocument(uri);
          vscode.window.showTextDocument(doc, { preview: false });
        }
      }),
      vscode.workspace.onDidSaveTextDocument(async (doc) => {
        const devicePath = deviceManager!.getOpenFileMap().get(doc.fileName);
        if (devicePath) {
          // 上传到设备，覆盖原文件
          await deviceManager!.writeFile(devicePath, doc.getText());
          vscode.window.showInformationMessage('已保存到设备');
        }
      }),
      vscode.workspace.onDidCloseTextDocument((doc) => {
        const devicePath = deviceManager!.getOpenFileMap().get(doc.fileName);
        if (devicePath) {
          try {
            fs.unlinkSync(doc.fileName);
          } catch (e) {
            // 忽略删除失败
          }
          deviceManager!.getOpenFileMap().delete(doc.fileName);
        }
      }),
      vscode.commands.registerCommand('mpy-studio.uploadToDevice', async (uri: vscode.Uri) => {
        if (!uri || !uri.fsPath) {
          vscode.window.showWarningMessage('未检测到本地文件/文件夹');
          return;
        }
        const stat = fs.statSync(uri.fsPath);
        const board = deviceManager!.getBoard();
        if (!board) {
          vscode.window.showWarningMessage('请先连接设备');
          return;
        }
        // 让用户选择目标目录
        const targetDir = await vscode.window.showInputBox({ prompt: '输入设备目标目录（如 / 或 /lib）', value: '/' });
        if (!targetDir) return;
        if (stat.isDirectory()) {
          // 递归上传文件夹
          const uploadFolder = async (localFolder: string, targetDir: string) => {
            if (!fs.existsSync(localFolder)) return;
            try { await board.fs_mkdir(targetDir); } catch {}
            const items = fs.readdirSync(localFolder, { withFileTypes: true });
            for (const item of items) {
              const localPath = nodePath.join(localFolder, item.name);
              const remotePath = nodePath.posix.join(targetDir, item.name);
              if (item.isDirectory()) {
                await uploadFolder(localPath, remotePath);
              } else {
                const content = fs.readFileSync(localPath);
                await board.fs_save(content.toString(), remotePath);
              }
            }
          };
          await uploadFolder(uri.fsPath, nodePath.posix.join(targetDir, nodePath.basename(uri.fsPath)));
        } else {
          const content = fs.readFileSync(uri.fsPath);
          const destPath = nodePath.posix.join(targetDir, nodePath.basename(uri.fsPath));
          await board.fs_save(content.toString(), destPath);
        }
        vscode.window.showInformationMessage('上传完成');
        deviceFolder.refresh();
      }),
      vscode.commands.registerCommand('mpy-studio.runOnDevice', async (uri: vscode.Uri) => {
        if (!uri || !uri.fsPath) {
          vscode.window.showWarningMessage('未检测到本地文件');
          return;
        }
        const filePath = uri.fsPath;
        const ext = nodePath.extname(filePath).toLowerCase();
        if (ext !== '.py') {
          vscode.window.showWarningMessage('只能运行 Python 文件');
          return;
        }
        let fileContent: string;
        try {
          fileContent = fs.readFileSync(filePath, 'utf-8');
        } catch (err) {
          vscode.window.showErrorMessage('读取文件失败: ' + (err instanceof Error ? err.message : String(err)));
          return;
        }
        try {
          // 如果未连接，自动弹出串口选择并连接
          if (!deviceManager!.isConnected()) {
            await deviceManager!.connect();
          }
        } catch (connErr) {
          vscode.window.showErrorMessage('设备连接失败: ' + (connErr instanceof Error ? connErr.message : String(connErr)));
          return;
        }
        try {
          await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `正在设备上运行 ${nodePath.basename(filePath)}`,
            cancellable: false
          }, async () => {
            await deviceManager!.run(fileContent);
          });
        } catch (err) {
          vscode.window.showErrorMessage('运行失败: ' + (err instanceof Error ? err.message : String(err)));
        }
      })
      // ...其它命令...
    );
    let replPanel: ReplPanel;
    let runner: Runner;

    try {
        // 2. 初始化依赖于 deviceFolder 的对象
        replPanel = new ReplPanel(context, deviceManager!);
        (deviceManager as any)._replPanel = replPanel;
        runner = new Runner(logger, deviceManager!);

        // 3. 加载配置
        await deviceManager!.loadConfig(context);

        // 4. 注册命令
        const commands = [
            vscode.commands.registerCommand('extension.updateTypings', async () => {
                try {
                    // 重新加载配置以更新类型定义
                    await deviceManager!.loadConfig(context);
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
                    const fileName = nodePath.basename(filePath);

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
                        await deviceManager!.fs_put(filePath, 'main.py', (msg) => {
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
                    showMessage('REPL面板未初始化,无法显示', 'error');
                    return;
                }

                    try {
                        await vscode.commands.executeCommand('mpy-studio.replPanel.focus');
                    } catch (focusError) {
                        showMessage('请手动打开 MPY-REPL 面板', 'warning');
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

                    // 添加 Python 选项到列表开头
                    const allOptions = [
                        {
                            label: 'Python (系统)',
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

            vscode.commands.registerCommand('mpy-studio.deleteFile', async (node: any) => {
                await deviceFolder.deleteFolderCommand(node);
            }),

            // 新建文件命令
            vscode.commands.registerCommand('mpy-studio.createFile', async (node: any) => {
                await deviceFolder.createFileCommand(node);
            }),

            // 新建文件夹命令
            vscode.commands.registerCommand('mpy-studio.createFolder', async (node: any) => {
                await deviceFolder.createFolderCommand(node);
            }),

            // 下载到本地命令
            vscode.commands.registerCommand('mpy-studio.downloadFile', async (node: any) => {
                if (!node || !node.fullPath) {
                    showMessage('未选中文件节点', 'warning');
                    return;
                }
                const ext = nodePath.extname(node.fullPath).toLowerCase();
                const fileName = nodePath.basename(node.fullPath);
                // 先弹出目录选择器
                const folderUris = await vscode.window.showOpenDialog({
                    canSelectFolders: true,
                    canSelectFiles: false,
                    canSelectMany: false,
                    openLabel: '选择保存文件夹'
                });
                if (!folderUris || folderUris.length === 0) return;
                const targetDir = folderUris[0].fsPath;
                const targetPath = nodePath.join(targetDir, fileName);
                try {
                    let content: Buffer | string;
                    if ([".png", ".jpg", ".jpeg", ".bmp", ".gif"].includes(ext)) {
                        // 图片/二进制
                        const bytes = await deviceManager!.getBoard()!.fs_cat_binary(node.fullPath);
                        if (!bytes) throw new Error('读取设备文件失败');
                        const arr = (typeof bytes === 'string' ? bytes : String(bytes)).split(',').filter(Boolean).map(Number);
                        content = Buffer.from(arr);
                        fs.writeFileSync(targetPath, content);
                    } else {
                        // 文本
                        content = await deviceManager!.loadFile(node.fullPath);
                        fs.writeFileSync(targetPath, content, 'utf8');
                    }
                    showMessage('文件已保存到本地: ' + targetPath, 'info');
                } catch (e) {
                    showMessage('下载失败: ' + (e instanceof Error ? e.message : String(e)), 'error');
                }
            }),
            vscode.commands.registerCommand('mpy-studio.refreshDevice', async () => {
              deviceFolder.refresh();
            }),
        ];
        context.subscriptions.push(...commands, outputChannel);

        // 注册 FileSystemProvider
        // 移除 TreeView provider 和相关命令注册

        // 6. 注册 REPL Webview（如有）
        if (replPanel) {
            context.subscriptions.push(
                vscode.window.registerWebviewViewProvider(
                    ReplPanel.viewType,
                    replPanel
                )
            );
            setTimeout(() => {
                try {
                    vscode.commands.executeCommand('mpy-studio.replPanel.focus');
                } catch (error) {
                    console.log('Failed to auto-focus REPL panel:', error);
                }
            }, 1000);
        }

        // 7. 初始化 TreeView context
        vscode.commands.executeCommand('setContext', 'mpyStudio.deviceConnected', false);

        // 8. 监听配置变化（如有需要）
        vscode.workspace.onDidChangeConfiguration(async (e) => {
            // 这里仅为示例，实际 context 变化监听需用 VSCode API 或轮询
        });
        vscode.window.onDidChangeWindowState(async (state) => {
            // 这里无法直接监听 context 变化，需在 connect/disconnect 后手动刷新
        });

        // 在 connect/disconnect 后刷新 TreeView
        // 建议在 DeviceManager.connect/disconnect 里调用 deviceFsProvider.refresh()
        // 并在 connect 后调用 deviceManager._board.fs_ls('/') 获取最新文件列表
        vscode.workspace.registerTextDocumentContentProvider('mpy-device', new DeviceTextDocumentContentProvider(deviceManager));
    } catch (error) {
        vscode.window.showErrorMessage(`mpy-studio扩展激活失败: ${error instanceof Error ? error.message : String(error)}`);
    }
}

export function deactivate() {
    deviceManager?.dispose();
}