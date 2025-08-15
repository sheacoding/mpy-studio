/**
 * 构建脚本 - 用于 GitHub Actions 中复制资源文件
 */
const fs = require('fs-extra');
const path = require('path');

async function copyResources() {
    const outDir = path.join(__dirname, 'out');
    
    // 确保输出目录存在
    await fs.ensureDir(outDir);
    
    // 复制 media 文件夹
    const mediaSource = path.join(__dirname, 'media');
    const mediaDest = path.join(outDir, 'media');
    if (await fs.pathExists(mediaSource)) {
        await fs.copy(mediaSource, mediaDest, { overwrite: true });
        console.log('✓ Copied media folder');
    }
    
    // 复制 typings 文件夹
    const typingsSource = path.join(__dirname, 'typings');
    const typingsDest = path.join(outDir, 'typings');
    if (await fs.pathExists(typingsSource)) {
        await fs.copy(typingsSource, typingsDest, { overwrite: true });
        console.log('✓ Copied typings folder');
    }
    
    console.log('Build resources copied successfully!');
}

// 执行复制
copyResources().catch(err => {
    console.error('Error copying resources:', err);
    process.exit(1);
});