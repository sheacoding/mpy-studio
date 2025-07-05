# MPBit Studio - MicroPython IDE

专为 ESP32 和 ESP32-S3 开发板设计的 VSCode MicroPython 扩展。

## ✨ 主要功能

- **设备管理**: 自动检测和连接 MicroPython 设备
- **代码执行**: 一键运行 Python 文件到设备
- **REPL 终端**: 集成交互式 MicroPython 终端
- **设备控制**: 重启、上传主程序、清除文件等操作

## 🚀 快速开始

1. **安装扩展**: 在 VSCode 扩展市场搜索 "MPBit Studio"
2. **连接设备**: 将 ESP32/ESP32-S3 通过 USB 连接到电脑
3. **运行代码**: 打开 Python 文件，点击运行按钮或使用命令面板

## 📋 核心功能

| 功能 | 描述 |
|------|------|
| 运行文件 | 执行当前 Python 文件到设备 |
| 停止程序 | 停止正在运行的程序 |
| REPL 终端 | 启动交互式 MicroPython 终端 |
| 上传主程序 | 将当前文件设为设备主程序 |
| 硬重启 | 完全重置设备状态 |
| 清除主程序 | 删除设备上的主程序文件 |
| 选择串口 | 选择设备连接端口 |

## 🎯 支持的开发板

- **ESP32**: ESP32-WROOM、ESP32-WROVER、ESP32-DevKitC 等
- **ESP32-S3**: ESP32-S3-DevKitC、ESP32-S3-WROOM 等

## 🔧 技术特性

- 基于 Arduino 官方 [micropython.js](https://github.com/arduino/micropython.js) 库
- TypeScript 实现，现代化架构
- 跨平台支持 (Windows/macOS/Linux)

---

**MPBit Studio** - 让 MicroPython 开发更简单！