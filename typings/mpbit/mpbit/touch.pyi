from machine import TouchPad
from typing import Optional, Callable


class Touch:
    """
    触摸按键控制类.
    """
    def __init__(self, pin) -> None:
        """
        初始化触摸按键.

        参数:
            pin (Any): 支持触摸的引脚对象(如Pin(4)).
        """
        ...

    def config(self, threshold: int) -> None:
        """
        设置触摸灵敏度阈值.

        参数:
            threshold (int): 触摸检测阈值.
        """
        ...

    def is_pressed(self) -> bool:
        """
        判断当前是否被按下.

        返回:
            (bool): True 表示正在被按下.
        """
        ...

    def was_pressed(self) -> bool:
        """
        判断是否曾经被按下过(该状态会被清除).

        返回:
            (bool): True 表示曾被按下.
        """
        ...

    def get_pressed(self) -> int:
        """
        获取累计被按下的次数(该计数会被清零).

        返回:
            (int): 按下次数.
        """
        ...

    def read(self) -> int:
        """
        读取当前触摸值.

        返回:
            (int): 触摸强度值.
        """
        ...

    @property
    def on_pressed(self) -> Optional[Callable[[int], None]]:
        """
        获取按下时的回调函数.

        返回:
            (Optional[Callable[[int], None]]): 回调函数.
        """
        ...

    @on_pressed.setter
    def on_pressed(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置按下时的回调函数.

        参数:
            callback (Optional[Callable[[int], None]]): 回调函数,接受一个参数(当前值).
        """
        ...

    @property
    def on_released(self) -> Optional[Callable[[int], None]]:
        """
        获取释放时的回调函数.

        返回:
            (Optional[Callable[[int], None]]): 回调函数.
        """
        ...

    @on_released.setter
    def on_released(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置释放时的回调函数.

        参数:
            callback (Optional[Callable[[int], None]]): 回调函数,接受一个参数(当前值).
        """
        ...