from machine import Pin
from typing import Optional, Callable


class Button:
    def __init__(self, pin_num: int, reverse: bool = False) -> None:
        """
        初始化按钮对象
        Args:
            pin_num: 引脚编号
            reverse: 是否反转电平（True 表示按下为高电平）
        """
        ...

    @property
    def on_pressed(self) -> Optional[Callable[[Pin], None]]:
        """获取按下时的回调函数"""
        ...

    @on_pressed.setter
    def on_pressed(self, callback: Optional[Callable[[Pin], None]]) -> None:
        """
        设置按下时的回调函数
        Args:
            callback: 回调函数，接受一个 Pin 参数
        """
        ...

    @property
    def on_released(self) -> Optional[Callable[[Pin], None]]:
        """获取释放时的回调函数"""
        ...

    @on_released.setter
    def on_released(self, callback: Optional[Callable[[Pin], None]]) -> None:
        """
        设置释放时的回调函数
        Args:
            callback: 回调函数，接受一个 Pin 参数
        """
        ...

    def is_pressed(self) -> bool:
        """判断当前按钮是否被按下"""
        ...

    def was_pressed(self) -> bool:
        """判断按钮是否曾经被按下过（该状态会被清除）"""
        ...

    def get_pressed(self) -> int:
        """获取按钮被按下的次数（该计数会被清零）"""
        ...

    def value(self) -> int:
        """获取当前按钮的电平值（0 或 1）"""
        ...

    def status(self) -> int:
        """
        获取按钮状态（0 表示未按下，1 表示已按下）
        注意：与 value() 相比做了逻辑反转
        """
        ...

    def irq(self, *args, **kwargs) -> None:
        """
        设置或操作底层引脚中断
        Args:
            *args: 传递给 Pin.irq 的参数
            **kwargs: 传递给 Pin.irq 的关键字参数
        """
        ...