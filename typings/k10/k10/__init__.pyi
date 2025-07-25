"""
K10 开发板模块

提供K10开发板相关的功能模块, 包括显示屏控制和IO扩展器
"""

import machine
from typing import Callable
from k10.pool import Pool
from neopixel import NeoPixel
from k10.button import Button
from k10.i2s_mic import I2SMic
from k10.i2s_speaker import I2SSpeaker
from k10.tca9555 import TCA9555
from k10.screen import Screen
from k10.tfcard import TFCard

i2c: machine.I2C
pool: Pool
rgb: NeoPixel
button_a:Button
button_b:Button
mic: I2SMic
speaker: I2SSpeaker
tca9555: TCA9555
screen: Screen
tf_card: TFCard

cleanup: Callable[[], None]
"""
软重启时自定义释放
"""
