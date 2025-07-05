# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional

# this class is used as a template for writing the mechanism that is
# used to store the touch screen calibration data. All properties and functions
# seen in this class need to exist in the class that is written to store the
# touch calibration data.

# For more information on how to do this see the touch calibration for the ESP32

class TouchCalData(object):

    def __init__(self, name):
        """
        初始化触摸校准数据
        
        参数:
            name: 校准数据名称
        返回:
            (None): 无返回值
        """
        ...
    
    def save(self):
        """
        保存校准数据
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    @property
    def left(self) -> Optional[int]:
        """
        获取左边界值
        
        参数:
            无
        返回:
            (Optional[int]): 左边界值
        """
        ...

    @left.setter
    def left(self, value: int):
        """
        设置左边界值
        
        参数:
            value (int): 左边界值
        返回:
            (None): 无返回值
        """
        ...

    @property
    def right(self) -> Optional[int]:
        """
        获取右边界值
        
        参数:
            无
        返回:
            (Optional[int]): 右边界值
        """
        ...

    @right.setter
    def right(self, value: int):
        """
        设置右边界值
        
        参数:
            value (int): 右边界值
        返回:
            (None): 无返回值
        """
        ...

    @property
    def top(self) -> Optional[int]:
        """
        获取上边界值
        
        参数:
            无
        返回:
            (Optional[int]): 上边界值
        """
        ...

    @top.setter
    def top(self, value: int):
        """
        设置上边界值
        
        参数:
            value (int): 上边界值
        返回:
            (None): 无返回值
        """
        ...

    @property
    def bottom(self) -> Optional[int]:
        """
        获取下边界值
        
        参数:
            无
        返回:
            (Optional[int]): 下边界值
        """
        ...

    @bottom.setter
    def bottom(self, value: int):
        """
        设置下边界值
        
        参数:
            value (int): 下边界值
        返回:
            (None): 无返回值
        """
        ...

    def reset(self):
        """
        重置校准数据
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...
