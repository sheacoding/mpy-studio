# MicroPython Studio Extension

一个简洁的 VSCode MicroPython 扩展，专注于串口设备管理和代码执行。

## 核心功能

- **设备管理**: 自动扫描和选择 MicroPython 设备串口
- **代码执行**: 通过 raw REPL 协议运行 Python 文件
- **设备重置**: 支持软重置和硬重置
- **文件操作**: 上传文件到设备并清除主程序
- **REPL 终端**: 集成 mpremote 终端支持

## 主要类

### DeviceManager
- 管理串口设备连接
- 处理状态栏显示
- 提供设备选择接口
- 基于官方 [micropython.js](https://github.com/arduino/micropython.js) 库

### Runner  
- 执行 Python 文件
- 管理设备重置和清除操作
- 处理运行结果输出

### Logger
- 统一日志输出管理
- 支持文件和控制台输出
- 提供时间戳和格式化

## 依赖库

- **micropython.js**: Arduino 官方的 MicroPython 通信库
- **serialport**: 串口通信支持
- **about-window**: 关于窗口组件

## 使用方式

1. 选择 MicroPython 设备串口
2. 打开 Python 文件
3. 使用运行按钮执行代码
4. 通过状态栏查看设备状态

## 技术特点

- 简洁的代码结构，易于维护
- 统一的错误处理机制
- 完整的日志记录系统
- 现代化的 TypeScript 实现
- 基于官方 Arduino micropython.js 库，稳定可靠