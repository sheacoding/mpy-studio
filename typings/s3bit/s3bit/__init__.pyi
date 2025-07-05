"""
K10 开发板模块

提供K10开发板相关的功能模块, 包括显示屏控制和IO扩展器
"""

from k10.tca9555 import TCA9555
from k10.screen import Screen

tca9555:TCA9555
screen:Screen