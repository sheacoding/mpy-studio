# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, Tuple
import _indev_base


class KeypadDriver(_indev_base.IndevBase):
    _last_key: int = ...

    def __init__(self):
        """
        初始化键盘驱动
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def _get_key(self) -> Optional[Tuple[int, int]]:
        """
        从键盘读取按键
        
        此函数需要返回LV_KEY枚举之一
        
        参数:
            无
        返回:
            (Optional[Tuple[int, int]]): 如果没有按键则返回None,否则返回按键ID
            
        异常:
            NotImplimentedError: 如果键盘驱动中没有重写此方法
        """
        ...

    def reset_long_press(self) -> None:
        """
        重置长按
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...


