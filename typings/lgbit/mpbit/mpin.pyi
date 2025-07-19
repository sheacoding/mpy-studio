from typing import Optional, Tuple, Callable, Any
from machine import Pin, PWM, ADC


class PinMode:
    """
    引脚模式类.
    """
    IN: int  # 输入模式
    OUT: int  # 输出模式
    PWM: int  # PWM模式
    ANALOG: int  # 模拟输入模式
    OUT_DRAIN: int  # 开漏输出模式


class MPin:
    """
    引脚封装类.
    """

    P0  = 33
    P1  = 32
    P2  = 35
    P3  = 34
    P4  = 39
    P5  = 0
    P6  = 16
    P7  = 17
    P8  = 26
    P9  = 25
    P10 = 36
    P11 = 2
    P13 = 18
    P14 = 19
    P15 = 21
    P16 = 5
    P19 = 22
    P20 = 23
    P23 = 27
    P24 = 14
    P25 = 12
    P26 = 13
    P27 = 15
    P28 = 4

    # ESP32引脚映射表
    PINS_REMAP_ESP32: Tuple[int, ...]
    # 支持PWM的引脚列表
    PWM_PINS: Tuple[int, ...]

    def __init__(self, pin: int, mode: int = PinMode.IN, pull: Optional[int] = None) -> None:
        """
        初始化引脚.

        参数:
            pin (int): 引脚编号.
            mode (int): 引脚模式,默认为输入模式.
            pull (Optional[int]): 上下拉设置,None表示不设置.
        """
        ...

    def deinit(self) -> None:
        """
        释放引脚占用的硬件资源.
        """
        ...

    def irq(self, trigger: int, handler: Optional[Callable[[Pin], None]]) -> None:
        """
        注册中断回调函数.

        参数:
            trigger (int): 触发方式(上升沿/下降沿).
            handler (Optional[Callable[[Pin], None]]): 回调函数.
        """
        ...

    def on_analog_change(self, handler: Optional[Callable[[int], None]], threshold: int = 40, period: int = 20) -> None:
        """
        当模拟值发生变化超过阈值时,触发回调函数.

        参数:
            handler (Optional[Callable[[int], None]]): 回调函数.
            threshold (int): 变化阈值,默认 40.
            period (int): 检测周期(单位毫秒),默认 20ms.
        """
        ...

    def is_high(self) -> bool:
        """
        判断当前引脚是否为高电平.
        """
        ...

    def is_low(self) -> bool:
        """
        判断当前引脚是否为低电平.
        """
        ...

    def toggle(self) -> None:
        """
        翻转当前输出引脚的电平状态(仅适用于输出模式).
        """
        ...

    def detach_irq(self) -> None:
        """
        显式移除所有中断回调函数.
        """
        ...

    def value(self, *args: int) -> Optional[int]:
        """
        统一读写接口,兼容 MicroPython 风格.
        无参数调用时读取当前值;有参数调用时写入新值.
        """
        ...

    def read_digital(self) -> Optional[int]:
        """
        读取当前引脚的数字信号值(0 或 1).
        """
        ...

    def write_digital(self, value: int) -> None:
        """
        向当前引脚写入数字电平值.

        参数:
            value (int): 0 表示低电平,非 0 表示高电平.
        """
        ...

    def read_analog(self) -> Optional[int]:
        """
        读取当前引脚的模拟输入值(0 ~ 4095).
        """
        ...

    def write_analog(self, duty: int, freq: int = 1000) -> None:
        """
        设置 PWM 输出的 10 位精度脉宽值(0 ~ 1023),用于控制占空比.

        参数:
            duty (int): 10 位脉宽值,0 表示低电平,1023 表示高电平.
            freq (int): PWM 频率,单位 Hz,默认 1000Hz.
        """
        ...

    def write_analog_u16(self, duty: int, freq: int = 1000) -> None:
        """
        设置 PWM 输出的 16 位精度脉宽值(0 ~ 65535),用于控制占空比.

        参数:
            duty (int): 16 位脉宽值,0 表示低电平,65535 表示高电平.
            freq (int): PWM 频率,单位 Hz,默认 1000Hz.
        """
        ...

    def set_duty_percent(self, percent: float) -> None:
        """
        设置 PWM 输出的占空比百分比(0~100).

        参数:
            percent (float): 设置占空比(单位百分比0-100%).
        """
        ...

    @staticmethod
    def get_remap_pin(pin: int) -> int:
        """
        获取逻辑引脚对应的 ESP32 实际 GPIO 编号.

        参数:
            pin (int): 引脚编号.

        返回:
            (int): 映射后的实际引脚号.
        """
        ...