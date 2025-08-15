# MPY-Studio 项目文档

## 项目概述

MPY-Studio 是一个专为 ESP32/ESP32-S3 开发板设计的 VSCode MicroPython 扩展，提供完整的 MicroPython 开发体验。该项目主要使用 TypeScript 开发，通过串口与 MicroPython 设备进行通信。

### 基本信息
- **项目名称**: mpy-studio
- **版本**: 1.0.5
- **当前维护者**: ericoding (sheacoding@gmail.com)
- **原作者**: bright (flashpf@qq.com)
- **许可证**: MIT
- **当前仓库**: https://github.com/sheacoding/mpy-studio
- **Fork 来源**: https://gitee.com/ai_mpy/mpy-studio
- **支持的开发板**: ESP32, ESP32-S3, ESP8266, PyBoard, RP2040

## 技术栈

### 核心技术
- **开发语言**: TypeScript
- **运行环境**: VSCode Extension (Node.js >= 22.12.0)
- **VSCode API**: ^1.92.0

### 主要依赖
- **串口通信**: 
  - `serialport` ^13.0.0 - 串口通信库
  - `@serialport/bindings-cpp` ^13.0.1 - 串口原生绑定
  - `@serialport/parser-readline` ^13.0.0 - 行解析器
- **文件系统**: `fs-extra` ^11.3.0 - 增强文件操作
- **发布工具**: `vsce` ^2.15.0 - VSCode 扩展打包发布

### 开发依赖
- **TypeScript**: ^5.3.3
- **测试框架**: Mocha
- **构建工具**: copyfiles, rimraf

## 项目结构

```
mpy-studio/
├── src/                     # 源代码目录
│   ├── extension.ts        # 扩展主入口，命令注册和生命周期管理
│   ├── board.ts           # 设备管理器，处理串口连接和设备操作
│   ├── micropython.ts     # MicroPython 板级通信协议实现
│   ├── repl-panel.ts      # REPL 终端面板实现
│   ├── runner.ts          # 代码运行器，处理文件执行
│   ├── deviceFloder.ts    # 设备文件系统树视图
│   ├── logger.ts          # 日志系统
│   └── stubs.ts           # 类型定义管理
├── media/                  # 静态资源
│   ├── *.svg              # 图标文件
│   ├── *.woff/woff2       # 字体文件
│   └── terminal.css       # 终端样式
├── typings/               # MicroPython 类型定义
├── tools/                 # 工具脚本
│   └── typings.py        # 类型定义生成脚本
├── out/                   # 编译输出目录
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript 配置
└── justfile              # Just 任务配置

```

## 核心功能模块

### 1. 设备管理 (board.ts)
- **DeviceManager 类**: 管理设备连接、断开、重连
- 支持串口设备自动扫描和选择
- 状态栏显示连接状态
- 设备硬重启和软重启功能
- 文件上传/下载管理

### 2. MicroPython 通信协议 (micropython.ts)
- **MicroPythonBoard 类**: 实现与 MicroPython 设备的底层通信
- 支持 RAW REPL 和普通 REPL 模式
- 文件系统操作：列目录、创建/删除文件、读写文件
- 代码执行和中断处理
- 二进制文件传输

### 3. REPL 终端 (repl-panel.ts)
- **ReplPanel 类**: WebView 实现的交互式终端
- 支持代码输入和输出显示
- 历史命令记录
- 自动滚动和清屏功能
- 连接状态实时显示

### 4. 代码运行器 (runner.ts)
- **Runner 类**: 处理 Python 文件执行
- 支持运行当前文件
- 上传为主程序 (main.py)
- 中断正在运行的程序
- 清除设备上的主程序

### 5. 设备文件系统 (deviceFloder.ts)
- **DeviceFolder 类**: TreeDataProvider 实现
- 显示设备文件系统结构
- 支持文件/文件夹创建、删除、重命名
- 文件上传下载
- 右键菜单操作

### 6. 日志系统 (logger.ts)
- **Logger 类**: 统一的日志管理
- 支持多级日志：debug, info, warn, error
- 输出到 VSCode 输出面板
- 日志文件持久化

## 命令和功能

### 主要命令
| 命令 ID | 功能描述 | 快捷键/图标 |
|---------|---------|------------|
| `extension.mpyRUN` | 运行当前文件 | $(play) |
| `extension.mpyStop` | 停止当前程序 | $(debug-stop) |
| `extension.mpyREPL` | 打开 REPL 终端 | $(terminal) |
| `extension.mpyMAIN` | 上传为主程序 | $(arrow-up) |
| `extension.mpyHardReset` | 硬重启设备 | $(debug-restart) |
| `extension.mpySelectPort` | 选择串口 | $(plug) |
| `extension.mpyDisconnect` | 断开连接 | $(debug-disconnect) |
| `extension.mpyDeviceFolder` | 打开设备文件夹 | $(folder) |
| `extension.selectBoard` | 选择开发板 | $(device-desktop) |
| `extension.updateTypings` | 更新类型定义 | $(sync) |

### 配置项
| 配置键 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `micropython.port` | string | "" | 串口设备路径 |
| `micropython.autoConnect` | boolean | false | 启动时自动连接 |
| `micropython.board` | string | "esp32" | 开发板类型 |
| `micropython.stubPath` | string | "" | 类型定义路径 |
| `mpy-studio.pureRepl.baudRate` | number | 115200 | 波特率 |
| `mpy-studio.pureRepl.timeout` | number | 2000 | 超时时间(ms) |
| `mpy-studio.showDebugInfo` | boolean | false | 显示调试信息 |

## 构建和开发

### 开发环境要求
- Node.js >= 22.12.0
- VSCode >= 1.92.0
- npm 或 yarn

### 构建脚本
```bash
# 安装依赖
npm install

# 编译 TypeScript
npm run compile

# 监听模式开发
npm run watch

# 打包扩展
npm run package

# 发布扩展
npm run publish

# 运行测试
npm test

# 代码检查
npm run lint
```

### 调试开发
1. 在 VSCode 中打开项目
2. 按 F5 启动调试会话
3. 会打开新的 VSCode 窗口用于测试扩展

## 使用流程

### 基本使用步骤
1. **安装扩展**: 从 VSCode 市场安装或使用 VSIX 文件
2. **连接设备**: 通过 USB 连接 ESP32/ESP32-S3 设备
3. **选择串口**: 点击状态栏选择对应串口
4. **选择开发板**: 点击状态栏选择开发板类型
5. **编写代码**: 创建 .py 文件编写 MicroPython 代码
6. **运行代码**: 右键菜单或命令面板执行代码

### 文件管理
- 通过设备文件夹视图管理设备文件
- 支持拖拽上传文件到设备
- 双击打开设备文件进行编辑
- 右键菜单提供完整文件操作

### REPL 交互
- 打开 REPL 面板进行实时交互
- 支持 Ctrl+C 中断程序
- Ctrl+D 软重启设备
- 历史命令通过上下键访问

## 注意事项

### 已知限制
1. 串口通信依赖系统驱动，需要正确安装设备驱动
2. 大文件传输可能需要较长时间
3. 某些操作系统可能需要额外权限访问串口

### 故障排除
1. **无法连接设备**: 检查串口驱动、USB 线缆、设备电源
2. **文件传输失败**: 确保设备有足够存储空间
3. **REPL 无响应**: 尝试硬重启设备
4. **类型提示不工作**: 执行"更新类型定义"命令

### 安全考虑
- 不要在设备上存储敏感信息
- 定期备份重要代码
- 注意串口权限设置

## 开发建议

### 代码风格
- 使用 TypeScript 严格模式
- 遵循 VSCode 扩展开发最佳实践
- 保持模块化和低耦合设计
- 添加充分的错误处理

### 测试策略
- 单元测试核心功能模块
- 集成测试设备通信流程
- 手动测试 UI 交互功能
- 多平台兼容性测试

### 性能优化
- 异步操作避免阻塞 UI
- 大文件分块传输
- 缓存常用数据减少设备查询
- 及时释放资源避免内存泄漏

## 贡献指南

欢迎提交 Issue 和 Pull Request：
- Bug 报告请提供详细复现步骤
- 新功能请先讨论可行性
- 代码提交需通过 lint 检查
- 更新相关文档和测试

## 联系方式

### 当前维护者
- GitHub: [@ericoding](https://github.com/ericoding)
- GitHub Issues: https://github.com/sheacoding/mpy-studio/issues
- Email: sheacoding@gmail.com

### 原项目
- 原项目地址: https://gitee.com/ai_mpy/mpy-studio
- 原作者 QQ: 370995782
- 原作者 Email: flashpf@qq.com