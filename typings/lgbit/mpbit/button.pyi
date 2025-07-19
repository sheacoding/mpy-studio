from machine import Pin
from typing import Optional, Callable, Any


class Button:
    """
    按钮控制类,用于处理按钮的各种状态和事件.
    """
    def __init__(self, pin_num: int, reverse: bool = False) -> None:
        """
        初始化按钮对象.

        参数:
            pin_num (int): 引脚编号.
            reverse (bool): 是否反转电平(True表示按下为高电平).
        """
        ...

    @property
    def on_pressed(self) -> Optional[Callable[[Pin], None]]:
        """
        获取按下时的回调函数.

        返回:
            (Optional[Callable[[Pin], None]]): 回调函数.
        """
        ...

    @on_pressed.setter
    def on_pressed(self, callback: Optional[Callable[[Pin], None]]) -> None:
        """
        设置按下时的回调函数.

        参数:
            callback (Optional[Callable[[Pin], None]]): 回调函数,接受一个Pin参数.
        """
        ...

    @property
    def on_released(self) -> Optional[Callable[[Pin], None]]:
        """
        获取释放时的回调函数.

        返回:
            (Optional[Callable[[Pin], None]]): 回调函数.
        """
        ...

    @on_released.setter
    def on_released(self, callback: Optional[Callable[[Pin], None]]) -> None:
        """
        设置释放时的回调函数.

        参数:
            callback (Optional[Callable[[Pin], None]]): 回调函数,接受一个Pin参数.
        """
        ...

    def is_pressed(self) -> bool:
        """
        判断当前按钮是否被按下.

        返回:
            (bool): 是否被按下.
        """
        ...

    def was_pressed(self) -> bool:
        """
        判断按钮是否曾经被按下过(该状态会被清除).

        返回:
            (bool): 是否曾经被按下过.
        """
        ...

    def get_pressed(self) -> int:
        """
        获取按钮被按下的次数(该计数会被清零).

        返回:
            (int): 按钮被按下的次数.
        """
        ...

    def value(self) -> int:
        """
        获取当前按钮的电平值(0或1).

        返回:
            (int): 当前按钮的电平值(0或1).
        """
        ...

    def status(self) -> int:
        """
        获取按钮状态(0表示未按下,1表示已按下).

        返回:
            (int): 按钮状态(0表示未按下,1表示已按下).
        注意: 与value()相比做了逻辑反转.
        """
        ...

    def irq(self, *args, **kwargs) -> None:
        """
        设置或操作底层引脚中断.

        参数:
            *args (Any): 传递给 Pin.irq 的参数.
            **kwargs (Any): 传递给 Pin.irq 的关键字参数.
        """
        ...