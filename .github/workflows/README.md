# GitHub Actions 工作流说明

本项目使用 GitHub Actions 实现自动化构建、测试和发布。

## 工作流文件

### 1. build.yml - 自动构建和测试
- **触发条件**:
  - 推送到 `main` 或 `ericoding-fork` 分支
  - Pull Request 到 `main` 分支
  - 手动触发
- **功能**:
  - 在多个操作系统（Ubuntu、Windows、macOS）上构建
  - 测试多个 Node.js 版本（18.x、20.x、22.x）
  - 编译 TypeScript 代码
  - 运行代码检查
  - 打包扩展为 VSIX 文件
  - 自动上传构建产物

### 2. release.yml - 版本发布
- **触发条件**:
  - 推送带有 `v*.*.*` 格式的标签（如 `v1.0.6`）
  - 手动触发并指定版本号
- **功能**:
  - 自动创建 GitHub Release
  - 生成发布说明
  - 上传 VSIX 安装包
  - 支持预发布版本

### 3. publish.yml - 发布到 VSCode Marketplace
- **触发条件**:
  - GitHub Release 发布后
  - 手动触发
- **功能**:
  - 自动发布到 VSCode Marketplace（需要配置密钥）
  - 保存 VSIX 文件作为构建产物

## 使用方法

### 自动构建
每次推送代码到主分支时会自动触发构建，无需额外操作。

### 发布新版本

#### 方法一：使用 Git 标签（推荐）
```bash
# 创建并推送版本标签
git tag v1.0.6
git push origin v1.0.6
```

#### 方法二：手动触发
1. 进入 GitHub 仓库的 Actions 页面
2. 选择 "Release" 工作流
3. 点击 "Run workflow"
4. 输入版本号（如 1.0.6）
5. 选择是否为预发布版本
6. 点击运行

### 查看构建产物
1. 进入 GitHub 仓库的 Actions 页面
2. 点击最近的构建记录
3. 在页面底部找到 "Artifacts" 部分
4. 下载 VSIX 文件

## 配置说明

### 发布到 VSCode Marketplace（可选）
如果需要自动发布到 VSCode Marketplace：

1. 获取 Personal Access Token
   - 访问 https://dev.azure.com
   - 创建新的 Personal Access Token
   - 勾选 "Marketplace > Publish" 权限

2. 配置 GitHub Secret
   - 进入仓库的 Settings > Secrets and variables > Actions
   - 点击 "New repository secret"
   - 名称：`VSCE_PAT`
   - 值：你的 Personal Access Token

## 构建状态徽章

在 README 中添加以下徽章显示构建状态：

```markdown
![Build Status](https://github.com/sheacoding/mpy-studio/workflows/Build%20and%20Test/badge.svg)
![Release](https://github.com/sheacoding/mpy-studio/workflows/Release/badge.svg)
```

## 故障排除

### 构建失败
- 检查 Node.js 版本要求（需要 >= 22.12.0）
- 确保所有依赖都已正确安装
- 查看 Actions 日志了解详细错误信息

### 发布失败
- 确保版本号格式正确（x.y.z）
- 检查是否有权限创建 Release
- 确认 package.json 中的版本号是否需要更新

## 注意事项

- VSIX 文件会自动保存 30-90 天
- 每次发布会自动创建 GitHub Release
- 支持同时在多个平台上构建测试
- 构建产物可以直接在 VSCode 中安装使用