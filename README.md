# MPBit Studio

MPBit Studio 是一个为 ESP32 和 MPBit 开发板设计的 MicroPython IDE 插件。它提供了完整的 MicroPython 开发环境，支持代码编写、运行、调试等功能。

## 功能特性

- 🔌 自动识别并连接 MicroPython 设备
- 📝 支持 MicroPython 代码编辑和语法提示
- ⚡ 快速运行当前 Python 文件
- 🔄 支持文件上传到开发板
- 💻 集成 REPL 终端

## 快速开始

1. 在 VS Code 中安装 MPBit Studio 插件
2. 点击工具栏中的 "选择串口" 按钮连接设备
3. 开始编写和运行 MicroPython 代码

## 主要命令

- `运行当前文件`: 在开发板上运行当前 Python 文件
- `上传当前文件`: 将当前文件上传到开发板
- `打开 REPL`: 打开 MicroPython 交互终端
- `选择串口`: 选择并连接设备
- `清除程序`: 清除开发板上运行的程序
- `断开连接`: 断开与设备的连接

## 配置选项

可以在 VS Code 设置中配置以下选项：

- `micropython.port`: 串口设备路径
- `micropython.board`: 开发板类型 (esp32/esp8266/pyboard/rp2040)
- `micropython.autoConnect`: 启动时自动连接设备
- `micropython.autoReconnect`: 设备断开时自动重连

## 开发要求

- VS Code 1.85.0 或更高版本
- Node.js
- Python 3.x

## 开发构建

```bash
npm install
npm run compile
```

## 许可证

[MIT License](LICENSE)