# mpy-studio 发布指南

## 📋 发布前检查清单

### 1. 代码质量检查
- [ ] 所有TypeScript代码编译通过
- [ ] 没有ESLint错误
- [ ] 功能测试通过
- [ ] README.md 内容完整且准确

### 2. 配置文件检查
- [ ] `package.json` 中的版本号正确
- [ ] `publisher` 字段设置正确
- [ ] `description` 字段描述准确
- [ ] `categories` 分类合适
- [ ] `keywords` 关键词完整

### 3. 资源文件检查
- [ ] 所有图标文件存在且格式正确
- [ ] README.md 中的图片链接有效
- [ ] LICENSE 文件存在且内容正确

## 🚀 发布步骤

### 1. 安装发布工具
```bash
npm install -g @vscode/vsce
```

### 2. 登录到VSCode Marketplace
```bash
vsce login <publisher-name>
```

### 3. 构建和打包
```bash
# 清理并编译
npm run compile

# 创建包
npm run package
```

### 4. 测试本地安装
```bash
# 安装到本地VSCode测试
code --install-extension mpy-studio-0.0.6.vsix
```

### 5. 发布到商店
```bash
# 发布当前版本
npm run publish

# 或者发布新版本
npm run publish:patch  # 0.0.3 -> 0.0.4
npm run publish:minor  # 0.0.3 -> 0.1.0
npm run publish:major  # 0.0.3 -> 1.0.0
```

## 📝 版本管理

### 语义化版本
- **patch**: 修复bug (0.0.3 -> 0.0.4)
- **minor**: 新功能 (0.0.3 -> 0.1.0)
- **major**: 重大变更 (0.0.3 -> 1.0.0)

### 更新版本号
```bash
# 自动更新版本号并发布
vsce publish patch
vsce publish minor
vsce publish major
```

## 🔍 发布后检查

### 1. 商店页面
- [ ] 扩展页面显示正确
- [ ] 描述和截图正确
- [ ] 下载和安装正常

### 2. 功能测试
- [ ] 在干净的VSCode中安装测试
- [ ] 所有命令正常工作
- [ ] 配置项正确显示

### 3. 用户反馈
- [ ] 监控用户评论和问题
- [ ] 及时响应用户反馈
- [ ] 根据反馈改进功能

## 🛠️ 常见问题

### Q: 发布失败怎么办？
A: 检查以下项目：
- 网络连接是否正常
- 是否已正确登录
- package.json 格式是否正确
- 版本号是否已存在

### Q: 如何更新已发布的扩展？
A: 使用 `vsce publish` 命令，会自动更新版本号

### Q: 如何撤销发布？
A: VSCode Marketplace 不支持撤销发布，只能发布新版本修复问题

## 📞 获取帮助

- [VSCode Extension Marketplace](https://marketplace.visualstudio.com/)
- [VSCE 文档](https://github.com/microsoft/vscode-vsce)
- [VSCode Extension API](https://code.visualstudio.com/api) 