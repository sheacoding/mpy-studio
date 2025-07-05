import * as vscode from 'vscode';
import * as fs from 'fs-extra';
import * as path from 'path';
import { Logger } from './logger';

export class StubsManager {
    private _logger: Logger;
    private _context: vscode.ExtensionContext;

    constructor(context: vscode.ExtensionContext, logger: Logger) {
        this._context = context;
        this._logger = logger;
    }

    /**
     * 获取插件内置的 typings 路径
     */
    getExtensionTypingsPath(): string {
        return path.join(this._context.extensionPath, 'typings');
    }

    /**
     * 读取插件内置的 typings/config.json 配置
     */
    async loadConfig(): Promise<{ boards?: Record<string, any> }> {
        const configPath = path.join(this.getExtensionTypingsPath(), 'config.json');
        
        if (!fs.existsSync(configPath)) {
            throw new Error('未找到插件内置的 typings/config.json 配置文件');
        }

        try {
            const raw = fs.readFileSync(configPath, 'utf8');
            const config = JSON.parse(raw);
            
            if (!config.boards) {
                throw new Error('config.json 中缺少 boards 字段');
            }

            this._logger.debug(`成功读取配置，包含 ${Object.keys(config.boards).length} 个开发板`);
            return config;
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this._logger.error(`读取 typings/config.json 失败: ${errorMsg}`);
            throw new Error(`读取 typings/config.json 失败: ${errorMsg}`);
        }
    }

    /**
     * 获取当前开发板名称
     */
    async getCurrentBoard(): Promise<string> {
        try {
            const selectedBoardKey = await this.getSelectedBoard();
            
            // 特殊处理 python 选项
            if (selectedBoardKey === 'python') {
                return 'PYTHON';
            }
            
            // 读取配置以获取开发板的显示名称
            const config = await this.loadConfig();
            
            // 如果配置中有 boards 字段，尝试获取开发板的显示名称
            if (config.boards && config.boards[selectedBoardKey]) {
                const boardConfig = config.boards[selectedBoardKey];
                return (boardConfig as any).name || selectedBoardKey;
            }
            
            // 如果找不到配置，返回开发板键名
            return selectedBoardKey;
        } catch (error) {
            this._logger.warn(`获取开发板配置失败: ${error instanceof Error ? error.message : String(error)}`);
            // 如果出错，返回 PYTHON
            return 'PYTHON';
        }
    }

    /**
     * 检查插件内置的 typings 目录是否存在
     */
    isTypingsExists(): boolean {
        const configPath = path.join(this.getExtensionTypingsPath(), 'config.json');
        return fs.existsSync(configPath);
    }

    /**
     * 根据选择的开发板更新 Python 分析配置
     */
    async updateSettingsForBoard(boardKey: string, boardConfig?: any): Promise<void> {
        try {
            const pythonConfig = vscode.workspace.getConfiguration('python.analysis');
            const extensionTypingsPath = this.getExtensionTypingsPath();

            if (boardKey === 'python') {
                // 如果是 python，移除所有 MicroPython 相关配置，只保留原生 Python 支持
                this._logger.info('切换到 Python 模式，移除 MicroPython 配置');
                
                // 清除 MicroPython 相关设置
                await pythonConfig.update('stubPath', undefined, vscode.ConfigurationTarget.Workspace);
                await pythonConfig.update('typeshedPaths', undefined, vscode.ConfigurationTarget.Workspace);
                await pythonConfig.update('extraPaths', undefined, vscode.ConfigurationTarget.Workspace);
                
                // 保留基本的 Python 分析设置
                await pythonConfig.update('typeCheckingMode', 'basic', vscode.ConfigurationTarget.Workspace);
                await pythonConfig.update('diagnosticSeverityOverrides', {
                    'reportMissingModuleSource': 'none'
                }, vscode.ConfigurationTarget.Workspace);
            } else {
                // 如果是其他开发板，配置对应的 stubs
                if (!boardConfig || !boardConfig.stubs) {
                    throw new Error(`开发板 ${boardKey} 缺少 stubs 配置`);
                }

                this._logger.info(`切换到开发板 ${boardKey}，配置 stubs: ${boardConfig.stubs.join(', ')}`);
                
                // 设置 stubPath（使用第一个 stub）
                const primaryStub = boardConfig.stubs[0];
                await pythonConfig.update('stubPath', path.join(extensionTypingsPath, primaryStub), vscode.ConfigurationTarget.Workspace);
                
                // 设置 typeshedPaths（所有 stubs）
                const typeshedPaths = boardConfig.stubs.map((stub: string) => path.join(extensionTypingsPath, stub));
                await pythonConfig.update('typeshedPaths', typeshedPaths, vscode.ConfigurationTarget.Workspace);
                
                // 设置 extraPaths（所有 stubs）
                const extraPaths = boardConfig.stubs.map((stub: string) => path.join(extensionTypingsPath, stub));
                await pythonConfig.update('extraPaths', extraPaths, vscode.ConfigurationTarget.Workspace);
                
                // 保留基本设置
                await pythonConfig.update('typeCheckingMode', 'basic', vscode.ConfigurationTarget.Workspace);
                await pythonConfig.update('diagnosticSeverityOverrides', {
                    'reportMissingModuleSource': 'none'
                }, vscode.ConfigurationTarget.Workspace);
            }
            
            // 保存用户选择的开发板到配置中
            const mpConfig = vscode.workspace.getConfiguration('mpy-studio');
            await mpConfig.update('selectedBoard', boardKey, vscode.ConfigurationTarget.Workspace);
            
            this._logger.info(`已更新 Python 分析配置并保存用户选择`);
            
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            this._logger.error(`更新 Python 分析配置失败: ${errorMsg}`);
            throw new Error(`更新 Python 分析配置失败: ${errorMsg}`);
        }
    }

    /**
     * 获取用户选择的开发板
     */
    async getSelectedBoard(): Promise<string> {
        try {
            // 从配置中读取用户选择
            const mpConfig = vscode.workspace.getConfiguration('mpy-studio');
            const userSelectedBoard = mpConfig.get<string>('selectedBoard');
            
            if (userSelectedBoard) {
                // 验证用户选择的开发板是否在 config.json 中存在
                const config = await this.loadConfig();
                if (userSelectedBoard === 'python' || (config.boards && config.boards[userSelectedBoard])) {
                    this._logger.debug(`从配置中读取到用户选择的开发板: ${userSelectedBoard}`);
                    return userSelectedBoard;
                } else {
                    this._logger.warn(`用户选择的开发板 ${userSelectedBoard} 在配置中不存在，切换到 PYTHON 模式`);
                    return 'python';
                }
            }
            
            // 如果用户没有选择过，返回默认值
            this._logger.debug(`用户未选择过开发板，使用默认值: PYTHON`);
            return 'python';
            
        } catch (error) {
            this._logger.warn(`获取用户选择的开发板失败: ${error instanceof Error ? error.message : String(error)}`);
            // 如果出错，返回默认值
            return 'python';
        }
    }
} 