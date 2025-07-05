"""
WS2812 NeoPixel LED控制模块

该模块提供WS2818 NeoPixel LED的驱动

注意: 该模块仅默认包含在ESP8266 ESP32和RP2端口
在STM32 Pyboard等其他端口上 您可以使用 `mip` 安装 `neopixel` 包
或者直接从 `micropython-lib` 下载模块并复制到文件系统
"""

# MCU: {'variant': 'SPIRAM', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC-SPIRAM', 'mpy': 'v6.3', 'ver': '1.25.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.25.0'}
# Stubber: v1.25.0
from __future__ import annotations
from _typeshed import Incomplete
from _mpy_shed import _NeoPixelBase
from machine import Pin
from typing import Tuple
from typing_extensions import Awaitable, TypeAlias, TypeVar

_Color: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]

def bitstream(*args, **kwargs) -> Incomplete: ...

class NeoPixel(_NeoPixelBase):
    """
    该类存储连接到引脚的WS2812 LED灯带的像素数据
    应用程序应设置像素数据 然后在准备好更新灯带时调用 `NeoPixel.write` 方法

    使用示例:
        import neopixel

        # 32 LED灯带连接到X8
        p = machine.Pin.board.X8
        n = neopixel.NeoPixel(p, 32)

        # 绘制红色渐变
        for i in range(32):
            n[i] = (i * 8, 0, 0)

        # 更新灯带
        n.write()
    """

    ORDER: tuple = ()
    def write(self) -> None:
        """
        将当前像素数据写入灯带

        返回:
            (None): 无返回值
        """
        ...

    def fill(self, pixel: _Color, /) -> None:
        """
        将所有像素的值设置为指定的像素值 即RGB或RGBW元组

        参数:
            pixel (_Color): RGB或RGBW元组形式的像素值

        返回:
            (None): 无返回值
        """
        ...

    def __init__(self, pin: Pin, n: int, /, *, bpp: int = 3, timing: int = 1) -> None:
        """
        构造一个NeoPixel对象

        参数:
            pin (Pin): machine.Pin实例
            n (int): 灯带中的LED数量
            bpp (int): RGB LED为3 RGBW LED为4 默认为3
            timing (int): 400KHz LED为0 800kHz LED为1 大多数为800kHz 默认为1

        返回:
            (None): 无返回值
        """
