import { Logger, LogLevel } from './logger';
import { DeviceManager } from './board';
import * as fs from 'fs';
import { ReplPanel } from './repl-panel';

export class Runner {
    private logger: Logger;
    private deviceManager: DeviceManager;
    private replPanel?: ReplPanel;

    constructor(logger: Logger, deviceManager: DeviceManager, replPanel?: ReplPanel) {
        this.logger = logger;
        this.deviceManager = deviceManager;
        this.replPanel = replPanel;
    }

    // 运行文件
    async runFile(filePath: string): Promise<boolean> {
        try {
            // 1. 读取文件内容
            let fileContent: string;
            try {
                fileContent = fs.readFileSync(filePath, 'utf-8');
                this.logger.info(`读取文件: ${filePath}`);
            } catch (err) {
                this.logger.error('读取文件失败: ' + (err instanceof Error ? err.message : String(err)));
                return false;
            }
            await this.deviceManager.connect();
            // 3. 获取提示符
            this.logger.debug('获取提示符...');
            await this.deviceManager.getPrompt();
            // 4. 运行代码
            this.logger.debug('开始运行代码...');
            const result = await this.deviceManager.run(fileContent);
            if (result) {
                this.logger.debug('代码运行结果:' + result);
            }
            return true;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : String(err);
            throw new Error(errorMessage);
        }
    }
    // 停止运行
    async stop(): Promise<void> {
        try {
            this.logger.debug(`停止运行`);
            await this.deviceManager.getPrompt();
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            throw new Error(errorMessage);
        }
    }

    // 清除主程序
    async clearMainPy(): Promise<void> {
        try {
            await this.stop();
            await this.deviceManager.fs_rm('/main.py');
            this.logger.info('已删除 main.py');
            this.logger.info('清除主程序完成');
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            throw new Error(errorMessage);
        }
    }
} 