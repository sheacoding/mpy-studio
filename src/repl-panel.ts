import * as vscode from 'vscode';
import { DeviceManager } from './board';

export class ReplPanel implements vscode.WebviewViewProvider {
    public static readonly viewType = 'mpy-studio.replPanel';
    private static readonly MAX_HISTORY_LINES = 200;

    private _view?: vscode.WebviewView;
    public deviceManager: DeviceManager;
    public _lastCommand: string = '';
    private _outputHistory: { text: string, type: string }[] = [];

    constructor(private readonly context: vscode.ExtensionContext, deviceManager: DeviceManager) {
        this.deviceManager = deviceManager;
    }

    reload() {
        this.setStatus(
            this.deviceManager.isConnected() ? `已连接: ${this.deviceManager.getCurrentPort()}` : '未连接',
            this.deviceManager.isConnected()
        );
        for (const item of this._outputHistory) {
            this._view?.webview.postMessage({ command: 'addOutput', text: item.text, type: item.type });
        }
    }

    resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;
        
        // 配置 webview 选项
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(this.context.extensionUri, 'media'),
                vscode.Uri.joinPath(this.context.extensionUri, 'out', 'media')
            ]
        };
        
        // 添加调试日志
        console.log('ReplPanel: Configuring webview with extensionUri:', this.context.extensionUri.fsPath);
        console.log('ReplPanel: Media path:', vscode.Uri.joinPath(this.context.extensionUri, 'media').fsPath);
        
        try {
            const html = this.getHtml(webviewView.webview);
            console.log('ReplPanel: Generated HTML successfully');
            webviewView.webview.html = html;
        } catch (error) {
            console.error('ReplPanel: Failed to generate webview HTML:', error);
            // 提供备用 HTML
            webviewView.webview.html = this.getFallbackHtml();
        }
        
        webviewView.onDidChangeVisibility(() => {
            if (webviewView.visible) {
                console.log('ReplPanel: Webview became visible, reloading...');
                this.reload();
            }
        });

        // 处理来自webview的消息
        webviewView.webview.onDidReceiveMessage(async (message) => {
            console.log('ReplPanel: Received message from webview:', message);
            switch (message.command) {
                case 'sendCommand':
                    try {
                        if (!this.deviceManager.isConnected()) {
                            this.addOutput('设备未连接，无法发送命令', 'error');
                            return;
                        }
                        let command = message.text + '\r';
                        this._lastCommand = message.text;
                        await this.deviceManager.sendCommand(command);
                    } catch (error) {
                        const errorMessage = error instanceof Error ? error.message : String(error);
                        this.addOutput(`发送命令失败: ${errorMessage}`, 'error');
                    }
                    break;
                case 'stop':
                    try {
                        if (!this.deviceManager.isConnected()) {
                            this.addOutput('设备未连接，无法发送中断信号', 'error');
                            return;
                        }
                        await this.deviceManager.getPrompt();
                    } catch (error) {
                        const errorMessage = error instanceof Error ? error.message : String(error);
                        this.addOutput(`停止失败:${errorMessage}`, 'error');
                    }
                    break;
                case 'clear':
                    this.clearOutput();
                    break;
                case 'connect': {
                    try {
                        this._lastCommand = ''
                        await this.deviceManager.connect();
                    } catch (err) {
                        console.error('ReplPanel: Connect error:', err);
                    }
                    break;
                }
                case 'disconnect':
                    try {
                        this._lastCommand = ''
                        await this.deviceManager.disconnect();
                    } catch (err) {
                        console.error('ReplPanel: Disconnect error:', err);
                    }
                    break;
            }
        });
    }

    private getHtml(webview: vscode.Webview): string {
        // 使用 webview.asWebviewUri 确保资源路径正确
        const styleUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.context.extensionUri, 'media', 'terminal.css')
        );
        const connectIconUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.context.extensionUri, 'media', 'connect.svg')
        );
        const disconnectIconUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.context.extensionUri, 'media', 'disconnect.svg')
        );
        const stopIconUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.context.extensionUri, 'media', 'stop.svg')
        );
        const deleteIconUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.context.extensionUri, 'media', 'delete.svg')
        );
        
        const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; img-src ${webview.cspSource} data:; script-src 'nonce-${webview.cspSource.split(' ')[0]}';">
    <title>MPY-REPL</title>
    <link rel="stylesheet" href="${styleUri}">
</head>
<body>
    <div class="terminal-container">
        <div class="terminal-header">
            <div class="connection-status">
                <button id="connectionStatusBtn" class="status-btn" title="连接状态">
                  <img id="connectionStatusIcon" src="${disconnectIconUri}" width="24" height="24" />
                </button>
                <span class="status-text" id="statusText">未连接</span>
            </div>
            <div class="terminal-controls">
                <button id="stopButton" class="status-btn" title="中断">
                  <img src="${stopIconUri}" class="icon" alt="中断" />
                </button>
                <button id="clearButton" class="status-btn" title="清空">
                  <img src="${deleteIconUri}" class="icon" alt="清空" />
                </button>
            </div>
        </div>
        <div class="terminal-content">
            <div class="terminal-output" id="terminalOutput"></div>
            <div class="terminal-input-line" id="terminalInputLine" style="display:none;">
                <span class="prompt">>>> </span>
                <input type="text" id="terminalInput" placeholder="输入命令..." disabled>
            </div>
        </div>
    </div>
    <script nonce="${webview.cspSource.split(' ')[0]}">
        const vscode = acquireVsCodeApi();
        const terminalOutput = document.getElementById('terminalOutput');
        const terminalInput = document.getElementById('terminalInput');
        const terminalInputLine = document.getElementById('terminalInputLine');
        const statusText = document.getElementById('statusText');
        const clearButton = document.getElementById('clearButton');
        const stopButton = document.getElementById('stopButton');
        const connectionStatusBtn = document.getElementById('connectionStatusBtn');
        const connectionStatusIcon = document.getElementById('connectionStatusIcon');
        const connectIconUri = ${JSON.stringify(connectIconUri.toString())};
        const disconnectIconUri = ${JSON.stringify(disconnectIconUri.toString())};
        let isConnected = false;

        // Robust DOMContentLoaded to ensure event binding
        function bindConnectBtn() {
            const btn = document.getElementById('connectionStatusBtn');
            if (!btn) {
                setTimeout(bindConnectBtn, 100); // Retry until DOM ready
                return;
            }
            btn.addEventListener('click', () => {
                if (isConnected) {
                    vscode.postMessage({ command: 'disconnect' });
                } else {
                    vscode.postMessage({ command: 'connect' });
                }
            });
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', bindConnectBtn);
        } else {
            bindConnectBtn();
        }

        stopButton.addEventListener('click', () => {
            vscode.postMessage({ command: 'stop' });
        });

        // 处理特殊的REPL输出格式
        function processReplOutput(text) {
            // 检测是否包含REPL提示符
            if (text.includes('>>>')) {
                return text;
            }
            
            // 检测错误信息
            if (text.includes('Traceback') || text.includes('Error:')) {
                return { text: text, type: 'error' };
            }
            
            // 检测raw REPL模式
            if (text.includes('raw REPL; CTRL-B to exit')) {
                return { text: text, type: 'info' };
            }
            
            // 检测OK响应
            if (text.startsWith('>OK')) {
                return { text: text, type: 'success' };
            }
            
            // 默认输出
            return { text: text, type: 'output' };
        }
        
        function addOutput(text, type = 'output') {
            // 简洁：如已连接，确保输入条显示
            if (isConnected) terminalInputLine.style.display = '';
            // 处理多行文本
            const lines = text.split('\\n');
            lines.forEach(line => {
                if (line === '') {
                    const emptyLine = document.createElement('div');
                    emptyLine.className = 'output-line';
                    emptyLine.innerHTML = '&nbsp;';
                    terminalOutput.appendChild(emptyLine);
                    return;
                }
                const lineElement = document.createElement('div');
                lineElement.className = 'output-line ' + type;
                if (line.startsWith(' ')) lineElement.style.whiteSpace = 'pre';
                lineElement.textContent = line;
                terminalOutput.appendChild(lineElement);
            });
            // 滚动到底部,确保DOM已渲染
            requestAnimationFrame(() => {
                terminalOutput.scrollTop = terminalOutput.scrollHeight;
            });
        }
        
        function clearOutput() {
            terminalOutput.innerHTML = '';
        }
        
        clearButton.addEventListener('click', () => {
            clearOutput();
            vscode.postMessage({ command: 'clear' });
        });
        
        terminalInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const command = terminalInput.value;
                if (command.trim()) {
                    // addOutput('>>> ' + command, 'input');
                    vscode.postMessage({ command: 'sendCommand', text: command });
                    saveToHistory(command);
                    terminalInput.value = '';
                }
            }
        });
        
        // 支持上下键浏览历史命令
        const commandHistory = [];
        let historyIndex = -1;
        
        terminalInput.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp') {
                if (historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    terminalInput.value = commandHistory[historyIndex];
                }
                e.preventDefault();
            } else if (e.key === 'ArrowDown') {
                if (historyIndex > 0) {
                    historyIndex--;
                    terminalInput.value = commandHistory[historyIndex];
                } else if (historyIndex === 0) {
                    historyIndex = -1;
                    terminalInput.value = '';
                }
                e.preventDefault();
            }
        });
        
        window.addEventListener('message', event => {
            const message = event.data;
            console.log('webview received message:', message);
            switch (message.command) {
                case 'addOutput':
                    // 处理特殊的REPL输出格式
                    const processed = processReplOutput(message.text);
                    if (typeof processed === 'object') {
                        addOutput(processed.text, processed.type);
                    } else {
                        addOutput(processed, message.type);
                    }
                    break;
                case 'clear':
                    clearOutput();
                    break;
                case 'setStatus':
                    statusText.textContent = message.text;
                    isConnected = !!message.connected;
                    connectionStatusIcon.src = isConnected ? connectIconUri : disconnectIconUri;
                    connectionStatusBtn.title = isConnected ? '点击断开连接' : '点击选择串口';
                    terminalInput.disabled = !isConnected;
                    if (isConnected) {
                        terminalInputLine.style.display = '';
                    } else {
                        terminalInputLine.style.display = 'none';
                    }
                    stopButton.disabled = !isConnected;
                    break;
            }
        });
        
        // 保存命令到历史记录
        function saveToHistory(command) {
            // 避免重复添加相同的命令
            if (commandHistory.length === 0 || commandHistory[0] !== command) {
                commandHistory.unshift(command);
                // 限制历史记录长度
                if (commandHistory.length > 50) {
                    commandHistory.pop();
                }
            }
            historyIndex = -1;
        }
    </script>
</body>
</html>`;
        return html;
    }

    private getFallbackHtml(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MPY-REPL</title>
    <style>
        body { font-family: monospace; margin: 0; padding: 10px; background: #1e1e1e; color: #d4d4d4; }
        .terminal-container { height: 100vh; display: flex; flex-direction: column; }
        .terminal-header { display: flex; justify-content: space-between; align-items: center; padding: 5px; border-bottom: 1px solid #333; }
        .terminal-content { flex: 1; overflow-y: auto; }
        .terminal-output { padding: 10px; }
        .output-line { margin: 2px 0; }
        .error { color: #f44336; }
        .success { color: #4caf50; }
        .info { color: #2196f3; }
        button { background: #333; color: #fff; border: 1px solid #555; padding: 5px 10px; cursor: pointer; }
        button:hover { background: #555; }
        input { background: #2d2d2d; color: #d4d4d4; border: 1px solid #555; padding: 5px; width: 100%; }
    </style>
</head>
<body>
    <div class="terminal-container">
        <div class="terminal-header">
            <div class="connection-status">
                <button id="connectionStatusBtn" title="连接状态">🔌</button>
                <span class="status-text" id="statusText">未连接</span>
            </div>
            <div class="terminal-controls">
                <button id="stopButton" title="中断">⏹</button>
                <button id="clearButton" title="清空">🗑</button>
            </div>
        </div>
        <div class="terminal-content">
            <div class="terminal-output" id="terminalOutput">
                <div class="output-line">REPL 终端加载中...</div>
            </div>
            <div class="terminal-input-line" id="terminalInputLine" style="display:none;">
                <span class="prompt">>>> </span>
                <input type="text" id="terminalInput" placeholder="输入命令..." disabled>
            </div>
        </div>
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        // 简化的 JavaScript 代码，确保基本功能可用
        document.getElementById('connectionStatusBtn').addEventListener('click', () => {
            vscode.postMessage({ command: 'connect' });
        });
        document.getElementById('stopButton').addEventListener('click', () => {
            vscode.postMessage({ command: 'stop' });
        });
        document.getElementById('clearButton').addEventListener('click', () => {
            document.getElementById('terminalOutput').innerHTML = '';
            vscode.postMessage({ command: 'clear' });
        });
        document.getElementById('terminalInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const command = e.target.value;
                if (command.trim()) {
                    vscode.postMessage({ command: 'sendCommand', text: command });
                    e.target.value = '';
                }
            }
        });
        window.addEventListener('message', event => {
            const message = event.data;
            const output = document.getElementById('terminalOutput');
            const statusText = document.getElementById('statusText');
            const terminalInput = document.getElementById('terminalInput');
            const terminalInputLine = document.getElementById('terminalInputLine');
            
            switch (message.command) {
                case 'addOutput':
                    const line = document.createElement('div');
                    line.className = 'output-line ' + (message.type || 'output');
                    line.textContent = message.text;
                    output.appendChild(line);
                    output.scrollTop = output.scrollHeight;
                    break;
                case 'clear':
                    output.innerHTML = '';
                    break;
                case 'setStatus':
                    statusText.textContent = message.text;
                    terminalInput.disabled = !message.connected;
                    if (message.connected) {
                        terminalInputLine.style.display = '';
                    } else {
                        terminalInputLine.style.display = 'none';
                    }
                    break;
            }
        });
    </script>
</body>
</html>`;
    }

    public addOutput(text: string, type: string = 'output') {
        if (this._lastCommand && text.startsWith(this._lastCommand)) {
            text = text.slice(this._lastCommand.length).trimStart();
            this._lastCommand = '';
            if (!text) return; // 如果去掉回显后没有内容，直接返回
        }
        this._outputHistory.push({ text, type });

        // 限制历史记录数量
        if (this._outputHistory.length > ReplPanel.MAX_HISTORY_LINES) {
            this._outputHistory = this._outputHistory.slice(-ReplPanel.MAX_HISTORY_LINES);
        }

        this._view?.webview.postMessage({ command: 'addOutput', text, type });
    }
    public clearOutput() {
        this._outputHistory.length = 0;
        this._view?.webview.postMessage({ command: 'clear' });
    }
    public setStatus(text: string, connected: boolean) {
        this._view?.webview.postMessage({ command: 'setStatus', text, connected });
    }
} 