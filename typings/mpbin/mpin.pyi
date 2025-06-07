from typing import Optional, Tuple, Callable, Any
from machine import Pin, PWM, ADC

class PinMode:
    """引脚模式类"""
    IN: int  # 输入模式
    OUT: int  # 输出模式
    PWM: int  # PWM模式
    ANALOG: int  # 模拟输入模式
    OUT_DRAIN: int  # 开漏输出模式

class MPin:
    """MicroPython 引脚控制类"""

    # ESP32引脚映射表
    PINS_REMAP_ESP32: Tuple[int, ...]
    # 支持PWM的引脚列表
    PWM_PINS: Tuple[int, ...]

    def __init__(self, pin: int, mode: int = PinMode.IN, pull: Optional[int] = None) -> None:
        """
        初始化引脚
        Args:
            pin: 引脚编号
            mode: 引脚模式，默认为输入模式
            pull: 上下拉设置，None表示不设置
        """
        ...

    def irq(self, trigger: int, handler: Callable[[Pin], None]) -> None:
        """
        设置引脚中断处理
        Args:
            trigger: 触发方式 (上升沿/下降沿)
            handler: 中断处理函数
        """
        ...

    def on_analog_change(self, handler: Optional[Callable[[int], None]], threshold: int = 40, period: int = 20) -> None:
        """
        设置模拟值变化回调
        Args:
            handler: 回调函数
            threshold: 触发阈值
            period: 检测周期(ms)
        """
        ...

    def read_digital(self) -> Optional[int]:
        """读取数字输入值"""
        ...

    def write_digital(self, value: int) -> None:
        """
        写入数字输出值
        Args:
            value: 输出值(0或1)
        """
        ...

    def read_analog(self) -> Optional[int]:
        """读取模拟值"""
        ...

    def write_analog(self, duty: int, freq: int = 1000) -> None:
        """
        写入PWM值
        Args:
            duty: 占空比(0-1023)
            freq: 频率(Hz)，默认1000Hz
        """
        ...

    @staticmethod
    def get_remap_pin(pin: int) -> int:
        """
        获取ESP32实际引脚映射
        Args:
            pin: 引脚编号
        Returns:
            映射后的实际引脚号
        """
        ...