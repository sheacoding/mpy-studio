import * as vscode from 'vscode';
import * as path from 'path';
import { DeviceManager } from './board';

export class DeviceNode extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly fullPath: string,
    public readonly isDir: boolean
  ) {
    super(label, collapsibleState);
    const ext = path.extname(label).toLowerCase();
    if (!isDir && ext === '.py') {
      this.contextValue = 'python';
    } else if (!isDir && ['.png', '.jpg', '.jpeg', '.bmp', '.gif'].includes(ext)) {
      this.contextValue = 'image';
    } else {
      this.contextValue = isDir ? 'folder' : 'file';
    }
    this.resourceUri = vscode.Uri.file(fullPath);
    this.iconPath = isDir
      ? new vscode.ThemeIcon('folder')
      : new vscode.ThemeIcon('file');
    // 不要设置 this.command
  }
}

export class DeviceFolder implements vscode.TreeDataProvider<DeviceNode> {
  private _onDidChangeTreeData: vscode.EventEmitter<DeviceNode | undefined | void> = new vscode.EventEmitter<DeviceNode | undefined | void>();
  readonly onDidChangeTreeData: vscode.Event<DeviceNode | undefined | void> = this._onDidChangeTreeData.event;
  private rootPath: string = '/'; // 保存根路径

  constructor(
    private deviceManager: DeviceManager,
    private context: vscode.ExtensionContext,
    private logger?: { info: Function; warn: Function; error: Function }
  ) {
    console.log("初始化设备文件夹")
  }


  async refresh(node?: DeviceNode): Promise<void> {
    this._onDidChangeTreeData.fire(node);
  }

  getTreeItem(element: DeviceNode): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: DeviceNode): Promise<DeviceNode[]> {
    const board = this.deviceManager.getBoard();
    if (!board || !board.serial || !board.serial.isOpen) {
      vscode.window.showWarningMessage('请先连接设备串口');
      return [];
    }
    let dir: string;
    if (!element) {
      // 根节点，动态获取根路径
      try {
        const code = "import sys; print('/flash' if '/flash' in sys.path else '/', end='')";
        await board.enter_raw_repl();
        const output = await board.exec_raw(code) as string;
        await board.exit_raw_repl();
        let str = typeof output === 'string' ? output : String(output);
        let okIdx = str.indexOf('OK');
        let endIdx = str.indexOf('\x04');
        if (okIdx !== -1 && endIdx !== -1 && endIdx > okIdx + 2) {
          dir = str.substring(okIdx + 2, endIdx).trim();
        } else {
          dir = str.trim();
        }
        this.rootPath = dir; // 保存根路径
      } catch (e) {
        vscode.window.showErrorMessage('获取设备根目录失败: ' + (e instanceof Error ? e.message : String(e)));
        return [];
      }
    } else {
      // 子节点，直接用 element.fullPath
      dir = element.fullPath;
    }
    try {
      // 只获取一层，调用 fs_ls
      const detailList = await board.fs_ls(dir);
      const files = detailList.map((f: any) => {
        const isDir = f.type === 'folder';
        return new DeviceNode(
          f.name,
          isDir ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.None,
          path.posix.join(dir, f.name),
          isDir
        );
      });
      // 文件夹在前，文件在后，同类型按名称排序
      files.sort((a: DeviceNode, b: DeviceNode) => {
        if (a.isDir !== b.isDir) {
          return a.isDir ? -1 : 1;
        }
        return a.label.localeCompare(b.label);
      });
      return files;
    } catch (e) {
      vscode.window.showErrorMessage('读取设备文件失败: ' + (e instanceof Error ? e.message : String(e)));
      return [];
    }
  }

  // 新建文件夹命令
  async createFolderCommand(node?: DeviceNode) {
    // 取选中节点路径，如果没有则用根路径
    let parentPath = this.rootPath || '/';
    if (node && typeof node.fullPath === 'string') {
      if ((node as DeviceNode).isDir) {
        parentPath = node.fullPath;
      } else {
        // 文件节点，取父目录
        parentPath = node.fullPath.substring(0, node.fullPath.lastIndexOf('/')) || '/';
      }
    }
    const folderName = await vscode.window.showInputBox({
      prompt: '输入新建文件夹名',
      placeHolder: 'new_folder'
    });
    if (!folderName) return;
    const board = this.deviceManager.getBoard();
    if (!board) return;
    try {
      const fullPath = path.posix.join(parentPath, folderName.replace(/'/g, "\\'"));
      await board.fs_mkdir(fullPath);
      // 总是刷新父目录
      let refreshTarget: DeviceNode | undefined = undefined;
      if (node && node.fullPath) {
        if ((node as DeviceNode).isDir) {
          refreshTarget = node;
        } else {
          // 文件节点，刷新其父目录
          const parentPath = node.fullPath.substring(0, node.fullPath.lastIndexOf('/')) || '/';
          refreshTarget = new DeviceNode(
            parentPath.split('/').pop() || '/',
            vscode.TreeItemCollapsibleState.Collapsed,
            parentPath,
            true
          );
        }
      }
      this.refresh(refreshTarget);
    } catch (e) {
      vscode.window.showErrorMessage('新建文件夹失败: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  // 新建文件命令
  async createFileCommand(node?: DeviceNode) {
    let parentPath = this.rootPath || '/';
    if (node && typeof node.fullPath === 'string') {
      parentPath = node.fullPath;
    }
    const fileName = await vscode.window.showInputBox({
      prompt: '输入新建文件名',
      placeHolder: 'example.py'
    });
    if (!fileName) return;
    const board = this.deviceManager.getBoard();
    if (!board) return;
    try {
      const fullPath = `${parentPath.replace(/'/g, "\\'")}/${fileName.replace(/'/g, "\\'")}`;
      await board.fs_put('', fullPath);
      vscode.window.showInformationMessage(`已创建文件: ${fileName}`);
      this.refresh();
    } catch (e) {
      vscode.window.showErrorMessage('新建文件失败: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  async deleteFolderCommand(node: DeviceNode) {
    const board = this.deviceManager.getBoard();
    if (!board || !node) return;
    try {
      if(node.isDir){
        // 先上传并执行 helpers.py
        const helpersPath = path.join(this.context.extensionPath, 'media', 'helpers.py');
        await board.execfile(helpersPath);
        // 调用 delete_folder(path)
        await board.run(`delete_folder('${node.fullPath}')`);
      }else{
        await board.fs_rm(node.fullPath);
      }
      // 计算父节点路径
      const parentPath = node.fullPath.substring(0, node.fullPath.lastIndexOf('/')) || '/';
      if (parentPath === this.rootPath) {
        this.refresh(undefined); // 刷新根节点
      } else {
        this.refresh(); // 全量刷新，保证UI一致
      }
    } catch (e) {
      vscode.window.showErrorMessage('删除文件夹失败: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  dispose() { }
}
