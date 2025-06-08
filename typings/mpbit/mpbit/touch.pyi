from machine import TouchPad
from typing import Optional, Callable


class Touch:
    def __init__(self, pin) -> None:
        """
        初始化触摸按键
        Args:
            pin: 支持触摸的引脚对象（如 Pin(4)）
        """
        ...

    def config(self, threshold: int) -> None:
        """
        设置触摸灵敏度阈值
        Args:
            threshold: 触摸检测阈值
        """
        ...

    def is_pressed(self) -> bool:
        """
        判断当前是否被按下
        Returns:
            bool: True 表示正在被按下
        """
        ...

    def was_pressed(self) -> bool:
        """
        判断是否曾经被按下过（该状态会被清除）
        Returns:
            bool: True 表示曾被按下
        """
        ...

    def get_pressed(self) -> int:
        """
        获取累计被按下的次数（该计数会被清零）
        Returns:
            int: 按下次数
        """
        ...

    def read(self) -> int:
        """
        读取当前触摸值
        Returns:
            int: 触摸强度值
        """
        ...

    @property
    def on_pressed(self) -> Optional[Callable[[int], None]]:
        """获取按下时的回调函数"""
        ...

    @on_pressed.setter
    def on_pressed(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置按下时的回调函数
        Args:
            callback: 回调函数，接受一个参数（当前值）
        """
        ...

    @property
    def on_released(self) -> Optional[Callable[[int], None]]:
        """获取释放时的回调函数"""
        ...

    @on_released.setter
    def on_released(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置释放时的回调函数
        Args:
            callback: 回调函数，接受一个参数（当前值）
        """
        ...