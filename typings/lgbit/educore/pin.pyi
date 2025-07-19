from typing import List, Optional, Callable

class pin:
    """
    引脚控制类.
    """
    def __init__(self, pin: int) -> None:
        """
        初始化一个引脚对象.

        参数:
            pin (int): 引脚编号.
        """
        ...

    def read_digital(self) -> int:
        """
        以数字方式读取引脚电平值.

        返回:
            (int): 引脚电平值,0(低)或 1(高).
        """
        ...

    def write_digital(self, value: int) -> None:
        """
        以数字方式向引脚写入电平值.

        参数:
            value (int): 要写入的值,0(低)或 1(高).
        """
        ...

    def read_analog(self) -> Optional[int]:
        """
        以模拟方式读取引脚电压值(仅限支持模拟输入的引脚).

        返回:
            (Optional[int]): 模拟值(0-4095),或根据数字电平返回 0/4095;不支持时返回 None.
        """
        ...

    def write_analog(self, value: int = 0, freq: int = 5000) -> None:
        """
        以 PWM 方式向引脚输出模拟信号.

        参数:
            value (int): 占空比(0-1023),默认为 0.
            freq (int): PWM 波形频率,默认为 5000 Hz.
        """
        ...

    def irq(self, handler: Optional[Callable[[], None]] = None, trigger: int = ...) -> None:
        """
        设置或清除引脚中断.

        参数:
            handler (Optional[Callable[[], None]]): 中断触发后调用的函数,无参数.
            trigger (int): 触发类型,例如 Pin.IRQ_RISING(上升沿),Pin.IRQ_FALLING(下降沿).
        """
        ...

    @property
    def event_change(self) -> Optional[Callable[[], None]]:
        """
        获取当前配置的引脚变化事件处理函数.

        返回:
            (Optional[Callable[[], None]]): 当前的事件处理函数.
        """
        ...

    @event_change.setter
    def event_change(self, new_event_change: Optional[Callable[[], None]]) -> None:
        """
        设置当引脚电平发生变化时的事件处理函数.

        参数:
            new_event_change (Optional[Callable[[], None]]): 新的事件处理函数.
        """
        ...

    @property
    def event_rising(self) -> Optional[Callable[[], None]]:
        """
        获取当前配置的上升沿事件处理函数.

        返回:
            (Optional[Callable[[], None]]): 当前的事件处理函数.
        """
        ...

    @event_rising.setter
    def event_rising(self, new_event_rising: Optional[Callable[[], None]]) -> None:
        """
        设置当检测到上升沿时的事件处理函数.

        参数:
            new_event_rising (Optional[Callable[[], None]]): 新的事件处理函数.
        """
        ...

    @property
    def event_falling(self) -> Optional[Callable[[], None]]:
        """
        获取当前配置的下降沿事件处理函数.

        返回:
            (Optional[Callable[[], None]]): 当前的事件处理函数.
        """
        ...

    @event_falling.setter
    def event_falling(self, new_event_falling: Optional[Callable[[], None]]) -> None:
        """
        设置当检测到下降沿时的事件处理函数.

        参数:
            new_event_falling (Optional[Callable[[], None]]): 新的事件处理函数.
        """
        ...