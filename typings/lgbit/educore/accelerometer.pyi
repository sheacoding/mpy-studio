from mpbit import accelerometer as _accelerometer
from typing import Optional


class accelerometer:
    """
    加速度传感器类,用于读取加速度值和检测摇晃状态.
    """

    def __init__(self):
        """
        初始化加速度传感器类.
        设置初始计数器和摇晃状态.
        启动定时器回调函数.
        """
        ...
    def accelerometer_callback(self):
        """
        加速度计回调函数,用于检测摇晃状态.
        """
        ...

    def X(self) -> int:
        """
        获取X轴加速度值.

        返回:
            (int): X轴加速度值.
        """
        ...

    def Y(self) -> int:
        """
        获取Y轴加速度值.

        返回:
            (int): Y轴加速度值.
        """
        ...

    def Z(self) -> int:
        """
        获取Z轴加速度值.

        返回:
            (int): Z轴加速度值.
        """
        ...

    def shake(self) -> bool:
        """
        获取摇晃状态.

        返回:
            (bool): 是否摇晃.
        """
        ...