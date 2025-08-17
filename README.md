# MPY-Studio

专为 ESP32/ESP32-S3 设计的 VSCode MicroPython 扩展，提供完整的开发体验。

> **Fork 来源**: 本项目 fork 自 [https://gitee.com/ai_mpy/mpy-studio](https://gitee.com/ai_mpy/mpy-studio)，感谢原作者的贡献！

![Version](https://img.shields.io/badge/version-1.0.6-blue.svg)
![MicroPython](https://img.shields.io/badge/MicroPython-1.26.0-green.svg)
![VSCode](https://img.shields.io/badge/VSCode-≥1.92.0-blueviolet.svg)
![Node.js](https://img.shields.io/badge/Node.js-≥22.12.0-green.svg)
![Fork](https://img.shields.io/badge/fork-ericoding-purple.svg)

## ✨ 核心功能

### 🎯 开发工具
- **智能代码**: MicroPython 语法提示、代码补全和类型检查
- **多板支持**: ESP32、ESP32-S3、行空板k10
- **文件管理**: 设备文件系统浏览、上传下载、在线编辑
- **REPL 终端**: 交互式 MicroPython 控制台

### 🚀 Wokwi 仿真 (v1.0.6 新增)
- **一键仿真**: 根据开发板类型自动生成 Wokwi 仿真链接
- **自动复制**: 自动复制当前 Python 代码到剪贴板
- **快速模式**: 无确认对话框，直接打开仿真
- **多板支持**: ESP32、ESP32-S3

### 📱 设备操作
- **串口管理**: 自动扫描和选择串口设备
- **文件传输**: 上传为主程序、批量文件传输
- **设备控制**: 硬重启、软重启、程序中断
- **状态监控**: 实时连接状态显示

## 🚀 快速开始

### 1. 安装扩展
```bash
# 从 VSCode 扩展市场搜索 "mpy-studio"
# 或手动安装 VSIX 文件
```

### 2. 连接设备
- 通过 USB 连接 ESP32/ESP32-S3 设备
- 点击状态栏选择对应串口
- 选择开发板类型

### 3. 开发代码
```python
# 创建 main.py 文件
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

### 4. 运行仿真
- 打开 Python 文件
- 点击 MicroPython 菜单中的 "模拟仿真" ⚡
- 代码会自动复制到剪贴板
- 在 Wokwi 中粘贴代码即可开始仿真

## 📋 主要命令

| 功能 | 命令 | 图标 | 说明 |
|------|------|------|------|
| 运行文件 | `extension.mpyRUN` | $(play) | 在设备上运行当前 Python 文件 |
| 停止程序 | `extension.mpyStop` | $(debug-stop) | 中断正在运行的程序 |
| REPL 终端 | `extension.mpyREPL` | $(terminal) | 打开交互式终端 |
| 上传主程序 | `extension.mpyMAIN` | $(arrow-up) | 上传为 main.py |
| 快速仿真 | `extension.wokwiQuickSimulation` | $(zap) | 一键复制代码并打开 Wokwi |
| 模拟仿真 | `extension.wokwiSimulation` | $(settings-gear) | 详细模式仿真 |
| 支持的板子 | `extension.wokwiShowBoards` | $(circuit-board) | 查看支持的开发板 |
| 选择开发板 | `extension.selectBoard` | $(device-desktop) | 切换开发板类型 |
| 设备重启 | `extension.mpyHardReset` | $(debug-restart) | 硬重启设备 |
| 设备文件 | `extension.mpyDeviceFolder` | $(folder) | 浏览设备文件系统 |

## 🛠️ 支持的开发板

| 开发板 | Wokwi 仿真链接 | 状态 |
|--------|----------------|------|
| **ESP32** | [micropython-esp32](https://wokwi.com/projects/new/micropython-esp32) | ✅ 完全支持 |
| **ESP32-S3** | [micropython-esp32s3](https://wokwi.com/projects/new/micropython-esp32s3) | ✅ 完全支持 |
| **ESP8266** | [micropython-esp8266](https://wokwi.com/projects/new/micropython-esp8266) | ✅ 完全支持 |
| **Raspberry Pi Pico** | [micropython-pi-pico](https://wokwi.com/projects/new/micropython-pi-pico) | ✅ 完全支持 |
| **PyBoard** | 使用 ESP32 模拟 | ⚠️ 部分支持 |

## 🔧 配置选项

```json
{
  "micropython.port": "",           // 串口设备路径
  "micropython.autoConnect": false, // 启动时自动连接
  "micropython.board": "esp32",     // 开发板类型
  "mpy-studio.pureRepl.baudRate": 115200,  // 波特率
  "mpy-studio.pureRepl.timeout": 2000,     // 超时时间(ms)
  "mpy-studio.showDebugInfo": false        // 显示调试信息
}
```

## 🎯 使用场景

### 本地开发
1. 在 VSCode 中编写 MicroPython 代码
2. 连接物理设备进行测试
3. 使用 REPL 进行交互式调试
4. 管理设备文件系统

### 在线仿真
1. 打开 Python 文件
2. 点击"快速仿真"按钮
3. 在 Wokwi 中粘贴代码
4. 添加硬件元件并运行仿真

### 协作开发
1. 代码编写完成后分享 Wokwi 链接
2. 团队成员可直接在浏览器中查看仿真
3. 无需安装任何软件即可测试代码

## 📈 版本历史

### v1.0.6 (最新)
- 🚀 **新增 Wokwi 仿真功能**
  - 简化的一键仿真体验
  - 自动复制代码到剪贴板
  - 支持多种开发板类型
- 🔧 **优化用户界面**
  - 整合仿真功能到主菜单
  - 使用不同图标区分功能
- ♻️ **代码重构**
  - 移除复杂模板系统
  - 优化项目结构

### v1.0.5
- 修复构建脚本和依赖问题
- 优化代码结构和性能

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境
```bash
# 克隆项目
git clone https://github.com/sheacoding/mpy-studio.git

# 安装依赖
npm install

# 开发模式
npm run watch

# 构建项目
npm run compile

# 打包扩展
npm run package
```

### 提交要求
- 遵循 TypeScript 严格模式
- 添加必要的错误处理
- 更新相关文档
- 通过所有检查

## 🐛 故障排除

### 常见问题
1. **设备无法连接**
   - 检查串口驱动是否安装
   - 确认 USB 线缆正常
   - 验证设备电源状态

2. **仿真无法打开**
   - 检查网络连接
   - 确认浏览器支持
   - 尝试手动访问 Wokwi

3. **代码无法运行**
   - 检查语法错误
   - 确认设备连接状态
   - 查看 REPL 输出信息

## 📚 参考资源

### 官方文档
- [MicroPython 官方文档](https://docs.micropython.org/)
- [Wokwi 仿真器文档](https://docs.wokwi.com/)
- [VSCode 扩展开发](https://code.visualstudio.com/api)

### 相关项目
- [MicroPython](https://github.com/micropython/micropython) - Python 微控制器实现
- [Arduino Lab MicroPython Editor](https://github.com/arduino/lab-micropython-editor) - Arduino 官方编辑器

## 📞 联系方式

### 当前维护者
- **GitHub**: [@ericoding](https://github.com/sheacoding)
- **邮箱**: sheacoding@gmail.com
- **项目地址**: [https://github.com/sheacoding/mpy-studio](https://github.com/sheacoding/mpy-studio)
- **问题反馈**: [Issues](https://github.com/sheacoding/mpy-studio/issues)

### 原项目作者
- **原项目地址**: [https://gitee.com/ai_mpy/mpy-studio](https://gitee.com/ai_mpy/mpy-studio)
- **作者**: bright (flashpf@qq.com)

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

**⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！**