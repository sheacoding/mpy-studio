# joystick.pyi
from typing import Callable, Optional
from timer_manager import TimerManager

class Joystick:
    """
    摇杆控制类,用于处理模拟摇杆的方向输入和按钮事件.
    
    支持:
        - 4方向检测(上下左右)
        - 8方向检测(含斜向)
        - 按钮按下/松开中断检测
    """

    # 方向常量
    NONE: int = ...
    LEFT: int = ...
    RIGHT: int = ...
    UP: int = ...
    DOWN: int = ...
    UP_LEFT: int = ...
    DOWN_LEFT: int = ...
    UP_RIGHT: int = ...
    DOWN_RIGHT: int = ...

    def __init__(self, vrx_pin: int, vry_pin: int, sw_pin: int) -> None:
        """
        初始化 Joystick 实例.

        参数:
            vrx_pin (int): X轴模拟输入引脚.
            vry_pin (int): Y轴模拟输入引脚.
            sw_pin (int): 按钮开关输入引脚.
        """
        ...

    def on_four_way(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置 4 方向变化时的回调函数.

        参数:
            callback (Optional[Callable[[int], None]]): 回调函数,接收一个方向参数.
        """
        ...

    def on_eight_way(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置 8 方向变化时的回调函数.

        参数:
            callback (Optional[Callable[[int], None]]): 回调函数,接收一个方向参数.
        """
        ...

    def on_pressed(self, callback: Optional[Callable[[bool], None]]) -> None:
        """
        设置按钮按下或松开时的回调函数.

        参数:
            callback (Optional[Callable[[bool], None]]): 回调函数,接收一个布尔参数表示是否按下.
        """
        ...