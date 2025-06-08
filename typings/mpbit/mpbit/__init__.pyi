from oled import OLED1106
from machine import I2C, ADC
from mpbit.mpin import MPin, PinMode
from qmi8658 import QMI8658
from mpbit.magnetic import Magnetic
from neopixel import NeoPixel
from mpbit.button import Button
from mpbit.touch import Touch

# I2C总线
i2c: I2C
# 板载I2C显示屏
oled: OLED1106
# 6轴传感器-加速度计
accelerometer: QMI8658.Accelerometer
# 6轴传感器-角速度计
gyroscope: QMI8658.Gyroscope
# 板载I2C磁力计传感器
magnetic: Magnetic
# 3个RGB LED灯带 Pin.P7
rgb: NeoPixel
# 光线传感器 Pin.P4 G39
light: ADC
# 板载声音传感器 Pin.P10 G36
sound: ADC
# 板载按键 A-Pin.P5-0,B-Pin.P11-2
button_a: Button
button_b: Button
# 触摸按键 P-Pin.P23-27,Y-Pin.P19-14,T-Pin.P25-12,H-Pin.P26-13,O-Pin.P27-15,N-Pin.P28-4
touchpad_p: Touch
touchpad_y: Touch
touchpad_t: Touch
touchpad_h: Touch
touchpad_o: Touch
touchpad_n: Touch

def number_map(
    value: float, from_low: float, from_high: float, to_low: float, to_high: float
) -> float:
    """
    数值映射函数，将一个范围内的数值映射到另一个范围
    参数:
        value (float): 要映射的数值
        from_low (float): 原范围的下限
        from_high (float): 原范围的上限
        to_low (float): 目标范围的下限
        to_high (float): 目标范围的上限
    返回:
        float: 映射后的数值
    """
    ...

def int_map(
    value: int, from_low: int, from_high: int, to_low: int, to_high: int
) -> int:
    """
    整数映射函数，将一个整数范围映射到另一个整数范围
    参数:
        value (int): 要映射的整数
        from_low (int): 原范围的最小值
        from_high (int): 原范围的最大值
        to_low (int): 目标范围的最小值
        to_high (int): 目标范围的最大值
    返回:
        int: 映射后的整数
    """
    ...

def get_i2c_bus(scl: int, sda: int, freq: int) -> I2C:
    """
    获取当前使用的 I2C 总线实例
    参数:
        scl: I2C 时钟线引脚编号
        sda: I2C 数据线引脚编号
        freq: I2C 总线频率
    返回:
        I2C: I2C 总线对象
    """
    ...

def i2c_has_addr(i2c_bus: I2C, addr: int) -> bool:
    """
    检查指定的 I2C 地址是否可用（设备是否存在）
    参数:
        i2c_bus (I2C): 要检查的 I2C 总线
        addr (int): 要检测的 I2C 设备地址
    返回:
        bool: 如果地址存在则返回 True，否则 False
    """
    ...

def uuid() -> str:
    """
    获取设备的唯一标识符（UUID）
    返回:
        str: 设备的唯一标识符
    """
    ...

__all__ = [
    "i2c",
    "oled",
    "accelerometer",
    "gyroscope",
    "magnetic",
    "rgb",
    "light",
    "sound",
    "button_a",
    "button_b",
    "touchpad_p",
    "touchpad_y",
    "touchpad_t",
    "touchpad_h",
    "touchpad_o",
    "touchpad_n",
    "get_i2c_bus",
    "i2c_has_addr",
    "number_map",
    "int_map",
    "uuid",
    "MPin",
    "PinMode",
    "OLED1106",
    "I2C",
    "ADC",
    "NeoPixel",
    "Button",
    "Magnetic",
    "Touch",
]
