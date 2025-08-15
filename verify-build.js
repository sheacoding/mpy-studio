/**
 * 构建验证脚本 - 检查构建后的文件是否完整
 */
const fs = require('fs');
const path = require('path');

function verifyBuild() {
    console.log('🔍 验证构建结果...\n');
    
    const outDir = path.join(__dirname, 'out');
    const requiredFiles = [
        'extension.js',
        'board.js',
        'micropython.js',
        'repl-panel.js',
        'runner.js'
    ];
    
    const requiredDirs = [
        'media',
        'typings'
    ];
    
    // 检查必要文件
    console.log('📁 检查编译文件:');
    let missingFiles = [];
    for (const file of requiredFiles) {
        const filePath = path.join(outDir, file);
        if (fs.existsSync(filePath)) {
            console.log(`  ✅ ${file}`);
        } else {
            console.log(`  ❌ ${file} (缺失)`);
            missingFiles.push(file);
        }
    }
    
    // 检查必要目录
    console.log('\n📂 检查资源目录:');
    let missingDirs = [];
    for (const dir of requiredDirs) {
        const dirPath = path.join(outDir, dir);
        if (fs.existsSync(dirPath)) {
            const files = fs.readdirSync(dirPath);
            console.log(`  ✅ ${dir} (${files.length} 个文件)`);
        } else {
            console.log(`  ❌ ${dir} (缺失)`);
            missingDirs.push(dir);
        }
    }
    
    // 检查依赖包
    console.log('\n📦 检查运行时依赖:');
    const nodeModulesDir = path.join(__dirname, 'node_modules');
    const requiredDeps = ['serialport', '@serialport', 'fs-extra', 'just'];
    let missingDeps = [];
    
    for (const dep of requiredDeps) {
        const depPath = path.join(nodeModulesDir, dep);
        if (fs.existsSync(depPath)) {
            console.log(`  ✅ ${dep}`);
        } else {
            console.log(`  ❌ ${dep} (缺失)`);
            missingDeps.push(dep);
        }
    }
    
    // 检查 package.json
    console.log('\n📋 检查 package.json:');
    const packagePath = path.join(__dirname, 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    console.log(`  ✅ 扩展名: ${packageJson.name}`);
    console.log(`  ✅ 版本: ${packageJson.version}`);
    console.log(`  ✅ 主入口: ${packageJson.main}`);
    
    // 总结
    console.log('\n📊 构建验证结果:');
    const hasIssues = missingFiles.length > 0 || missingDirs.length > 0 || missingDeps.length > 0;
    
    if (hasIssues) {
        console.log('  ❌ 构建不完整');
        if (missingFiles.length > 0) {
            console.log(`    缺失文件: ${missingFiles.join(', ')}`);
        }
        if (missingDirs.length > 0) {
            console.log(`    缺失目录: ${missingDirs.join(', ')}`);
        }
        if (missingDeps.length > 0) {
            console.log(`    缺失依赖: ${missingDeps.join(', ')}`);
        }
        process.exit(1);
    } else {
        console.log('  ✅ 构建完整，可以打包');
    }
}

verifyBuild();