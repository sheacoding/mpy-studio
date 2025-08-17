/**
 * 简化的Wokwi仿真功能
 * 直接根据开发板类型打开对应的Wokwi URL
 */

import * as vscode from 'vscode';

export class SimpleWokwi {
    
    /**
     * 获取当前选择的开发板类型
     */
    private getCurrentBoardType(): string {
        const config = vscode.workspace.getConfiguration();
        
        // 尝试从多个配置项获取开发板类型
        const selectedBoard = config.get<string>('mpy-studio.selectedBoard');
        const micropythonBoard = config.get<string>('micropython.board');
        
        // 优先使用用户选择的开发板
        if (selectedBoard && selectedBoard !== '' && selectedBoard !== 'python') {
            return selectedBoard;
        }
        
        // 其次使用micropython配置的开发板
        if (micropythonBoard && micropythonBoard !== '') {
            return micropythonBoard;
        }
        
        // 默认返回esp32
        return 'esp32';
    }
    
    /**
     * 根据开发板类型生成Wokwi URL
     */
    private generateWokwiUrl(boardType: string): string {
        const baseUrl = 'https://wokwi.com/projects/new/';
        
        switch (boardType.toLowerCase()) {
            case 'esp32':
                return baseUrl + 'micropython-esp32';
            case 'esp32s3':
            case 'esp32-s3':
                return baseUrl + 'micropython-esp32s3';
            case 'esp8266':
                return baseUrl + 'micropython-esp8266';
            case 'rp2040':
            case 'raspberry-pi-pico':
                return baseUrl + 'micropython-pi-pico';
            case 'pyboard':
                return baseUrl + 'micropython-esp32'; // Pyboard使用ESP32模拟
            default:
                return baseUrl + 'micropython-esp32'; // 默认ESP32
        }
    }
    
    /**
     * 获取开发板的显示名称
     */
    private getBoardDisplayName(boardType: string): string {
        switch (boardType.toLowerCase()) {
            case 'esp32':
                return 'ESP32';
            case 'esp32s3':
            case 'esp32-s3':
                return 'ESP32-S3';
            case 'esp8266':
                return 'ESP8266';
            case 'rp2040':
            case 'raspberry-pi-pico':
                return 'Raspberry Pi Pico';
            case 'pyboard':
                return 'PyBoard';
            default:
                return 'ESP32';
        }
    }
    
    /**
     * 打开Wokwi仿真 - 简化操作，自动复制代码
     * @param quickMode 是否使用快速模式（跳过确认对话框）
     */
    async openWokwiSimulation(quickMode: boolean = false): Promise<void> {
        try {
            // 检查当前是否有打开的Python文件
            const activeEditor = vscode.window.activeTextEditor;
            const hasPythonFile = activeEditor && 
                (activeEditor.document.languageId === 'python' || 
                 activeEditor.document.fileName.toLowerCase().endsWith('.py'));
            
            // 获取当前开发板类型
            const boardType = this.getCurrentBoardType();
            const boardName = this.getBoardDisplayName(boardType);
            const wokwiUrl = this.generateWokwiUrl(boardType);
            
            // 如果有Python文件，自动复制代码到剪贴板
            if (hasPythonFile) {
                const code = activeEditor!.document.getText();
                await vscode.env.clipboard.writeText(code);
                
                const fileName = activeEditor!.document.fileName;
                const shortFileName = fileName.split(/[\\\/]/).pop() || fileName;
                
                if (quickMode) {
                    // 快速模式：直接打开Wokwi，显示简单通知
                    await vscode.env.openExternal(vscode.Uri.parse(wokwiUrl));
                    
                    vscode.window.showInformationMessage(
                        `🚀 ${boardName}仿真已打开！代码已复制到剪贴板，在Wokwi中按Ctrl+V粘贴即可。`,
                        { modal: false }
                    );
                } else {
                    // 普通模式：显示确认信息
                    let message = `🚀 Wokwi仿真准备就绪！\n\n`;
                    message += `📱 开发板: ${boardName}\n`;
                    message += `📄 文件: ${shortFileName}\n`;
                    message += `📋 代码已自动复制到剪贴板\n\n`;
                    message += `🔧 接下来您只需要:\n`;
                    message += `1. 在Wokwi中粘贴代码 (Ctrl+V)\n`;
                    message += `2. 添加硬件元器件\n`;
                    message += `3. 连接电路并运行仿真`;
                    
                    const action = await vscode.window.showInformationMessage(
                        message,
                        '🚀 打开Wokwi',
                        '⚙️ 更换开发板',
                        '❌ 取消'
                    );
                    
                    if (action === '🚀 打开Wokwi') {
                        // 打开Wokwi URL
                        await vscode.env.openExternal(vscode.Uri.parse(wokwiUrl));
                        
                        // 显示简单的成功提示
                        setTimeout(() => {
                            vscode.window.showInformationMessage(
                                `✅ Wokwi已打开，代码已在剪贴板中！\n直接在main.py中按Ctrl+V粘贴即可开始仿真。`
                            );
                        }, 1000);
                    } else if (action === '⚙️ 更换开发板') {
                        await vscode.commands.executeCommand('extension.selectBoard');
                    }
                }
                
            } else {
                // 没有Python文件时的提示
                let message = `⚠️ 未检测到打开的Python文件\n\n`;
                message += `📱 当前开发板: ${boardName}\n`;
                message += `🌐 仿真链接: ${wokwiUrl}\n\n`;
                message += `💡 建议: 先打开一个.py文件，然后再使用模拟仿真功能`;
                
                const action = await vscode.window.showInformationMessage(
                    message,
                    '🚀 仍然打开Wokwi',
                    '⚙️ 更换开发板',
                    '❌ 取消'
                );
                
                if (action === '🚀 仍然打开Wokwi') {
                    await vscode.env.openExternal(vscode.Uri.parse(wokwiUrl));
                } else if (action === '⚙️ 更换开发板') {
                    await vscode.commands.executeCommand('extension.selectBoard');
                }
            }
            
        } catch (error) {
            vscode.window.showErrorMessage(`打开Wokwi仿真失败: ${error}`);
        }
    }
    
    /**
     * 快速仿真 - 一键复制代码并打开Wokwi（无确认对话框）
     */
    async quickSimulation(): Promise<void> {
        await this.openWokwiSimulation(true);
    }
    
    /**
     * 显示支持的开发板信息
     */
    async showSupportedBoards(): Promise<void> {
        const boardInfo = [
            '🔷 ESP32 → https://wokwi.com/projects/new/micropython-esp32',
            '🔶 ESP32-S3 → https://wokwi.com/projects/new/micropython-esp32s3', 
            '🔸 ESP8266 → https://wokwi.com/projects/new/micropython-esp8266',
            '🍓 Raspberry Pi Pico → https://wokwi.com/projects/new/micropython-pi-pico'
        ];
        
        const message = `🎯 支持的开发板和对应仿真链接:\n\n${boardInfo.join('\n')}\n\n💡 点击"更换开发板"可以切换当前开发板类型`;
        
        const action = await vscode.window.showInformationMessage(
            message,
            { modal: true },
            '⚙️ 更换开发板',
            '✅ 知道了'
        );
        
        if (action === '⚙️ 更换开发板') {
            await vscode.commands.executeCommand('extension.selectBoard');
        }
    }
}