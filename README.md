# MPBit Studio - MicroPython IDE

一个专为 MicroPython 开发设计的 VSCode 扩展，提供完整的设备管理、代码执行和 REPL 交互功能。

## ✨ 主要功能

### 🔌 智能设备管理
- **自动设备检测**: 自动扫描并识别 MicroPython 设备
- **多板卡支持**: 支持 ESP32、ESP8266、Raspberry Pi Pico 等多种开发板
- **持久化配置**: 记住您的设备选择，无需重复配置
- **状态监控**: 实时显示设备连接状态和类型

### 🚀 代码执行
- **一键运行**: 直接执行当前 Python 文件到设备
- **Raw REPL 协议**: 使用官方 MicroPython raw REPL 协议，稳定可靠
- **错误处理**: 智能错误提示和异常处理
- **输出显示**: 实时显示执行结果和错误信息

### 🔄 设备控制
- **软重置**: 安全重启 MicroPython 设备
- **硬重置**: 完全重置设备状态
- **文件管理**: 上传文件到设备并管理主程序
- **存储清理**: 清除设备上的主程序文件

### 💻 集成 REPL
- **WebView 终端**: 现代化的 REPL 交互界面
- **实时通信**: 与设备实时交互
- **命令历史**: 支持命令历史记录
- **语法高亮**: Python 代码语法高亮显示

## 🛠️ 快速开始

### 1. 安装扩展
在 VSCode 扩展市场中搜索 "MPBit Studio" 并安装。

### 2. 连接设备
1. 将 MicroPython 设备通过 USB 连接到电脑
2. 点击状态栏中的设备选择器
3. 选择您的设备（支持 ESP32、ESP8266、Pico 等）

### 3. 运行代码
1. 打开一个 Python 文件
2. 使用 `Ctrl+Shift+P` 打开命令面板
3. 选择 "MPBit Studio: Run Python File" 或点击运行按钮

### 4. 使用 REPL
1. 打开命令面板
2. 选择 "MPBit Studio: Open REPL"
3. 在 REPL 面板中与设备交互

## 📋 支持的功能

| 功能 | 描述 | 快捷键 |
|------|------|--------|
| 运行 Python 文件 | 执行当前文件到设备 | `Ctrl+Shift+P` → "Run Python File" |
| 打开 REPL | 启动交互式终端 | `Ctrl+Shift+P` → "Open REPL" |
| 软重置设备 | 安全重启设备 | `Ctrl+Shift+P` → "Soft Reset" |
| 硬重置设备 | 完全重置设备 | `Ctrl+Shift+P` → "Hard Reset" |
| 清除主程序 | 删除设备上的 main.py | `Ctrl+Shift+P` → "Clear Main" |

## 🎯 支持的开发板

- **ESP32**: ESP32-WROOM、ESP32-WROVER 等
- **ESP8266**: NodeMCU、Wemos D1 Mini 等  
- **Raspberry Pi Pico**: Pico、Pico W 等
- **其他 MicroPython 设备**: 支持所有运行 MicroPython 的开发板

## 🔧 技术特性

- **基于官方库**: 使用 Arduino 官方的 [micropython.js](https://github.com/arduino/micropython.js) 库
- **TypeScript 实现**: 现代化的代码架构，易于维护和扩展
- **统一日志系统**: 完整的日志记录和错误追踪
- **响应式 UI**: 现代化的用户界面设计
- **跨平台支持**: 支持 Windows、macOS 和 Linux

## 🚀 开发计划

- [ ] 文件管理器：直接在 VSCode 中管理设备文件
- [ ] 调试支持：集成 MicroPython 调试器
- [ ] 代码片段：常用 MicroPython 代码片段
- [ ] 项目模板：快速创建 MicroPython 项目
- [ ] 固件管理：设备固件升级和管理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**MPBit Studio** - 让 MicroPython 开发更简单、更高效！