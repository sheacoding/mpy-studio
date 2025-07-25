from typing import Callable, Optional

class Button:
    A = 2
    B = 12

    def __init__(self, type: int):
        """
        构造函数
        参数:
            type (int): 按钮类型(Button.A 或 Button.B)
        返回:
            (None): 无返回值
        """
        ...
    def deinit(self) -> None:
        """
        释放按钮资源
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    @property
    def on_pressed(self) -> Optional[Callable[[], None]]:
        """
        按钮按下事件回调属性
        参数:
            无
        返回:
            (Optional[Callable[[], None]]): 按下时调用的回调函数
        """
        ...
    @on_pressed.setter
    def on_pressed(self, callback: Optional[Callable[[], None]]) -> None:
        """
        设置按钮按下事件回调
        参数:
            callback (Optional[Callable[[], None]]): 按下时调用的回调函数
        返回:
            (None): 无返回值
        """
        ...

    @property
    def on_released(self) -> Optional[Callable[[], None]]:
        """
        按钮释放事件回调属性
        参数:
            无
        返回:
            (Optional[Callable[[], None]]): 释放时调用的回调函数
        """
        ...
    @on_released.setter
    def on_released(self, callback: Optional[Callable[[], None]]) -> None:
        """
        设置按钮释放事件回调
        参数:
            callback (Optional[Callable[[], None]]): 释放时调用的回调函数
        返回:
            (None): 无返回值
        """
        ...
