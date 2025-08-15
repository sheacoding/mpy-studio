import { Logger } from './logger';
import { DeviceManager } from './board';
import * as fs from 'fs';

export class Runner {
    private logger: Logger;
    private deviceManager: DeviceManager;

    constructor(logger: Logger, deviceManager: DeviceManager) {
        this.logger = logger;
        this.deviceManager = deviceManager;
    }

    // 运行文件
    async runFile(filePath: string): Promise<boolean> {
        try {
            let fileContent: string;
            try {
                fileContent = fs.readFileSync(filePath, 'utf-8');
                this.logger.info(`读取文件: ${filePath}`);
            } catch (err) {
                this.logger.error('读取文件失败: ' + (err instanceof Error ? err.message : String(err)));
                return false;
            }
            await this.deviceManager.connect();
            this.logger.debug('获取提示符...');
            await this.deviceManager.getPrompt();
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
            
            // 第一次尝试：发送中断信号停止程序（缩短超时时间）
            await this.deviceManager.stop();
            await new Promise(resolve => setTimeout(resolve, 300));
            
            try {
                // 尝试获取提示符确认停止成功（缩短超时到1秒）
                await Promise.race([
                    this.deviceManager.getPrompt(),
                    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 1000))
                ]);
                this.logger.info('程序已停止');
                return;
            } catch (timeoutError) {
                this.logger.warn('常规停止方法超时，直接使用软重启...');
            }
            
            // 第二次尝试：对于定时器程序，直接使用软重启（最有效的方法）
            try {
                this.logger.info('执行软重启停止程序...');
                await this.deviceManager.reset();
                await new Promise(resolve => setTimeout(resolve, 1500));
                this.logger.info('通过软重启成功停止程序');
                return;
            } catch (resetError) {
                this.logger.warn('软重启失败，尝试硬重启...');
            }
            
            // 最后尝试：硬重启设备
            await this.deviceManager.hard_reset();
            await new Promise(resolve => setTimeout(resolve, 2000));
            this.logger.info('通过硬重启停止程序');
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            this.logger.error(`停止程序失败: ${errorMessage}`);
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