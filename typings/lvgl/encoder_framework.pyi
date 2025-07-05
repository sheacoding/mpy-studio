# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Union, Optional, Tuple, ClassVar
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import lvgl as lv  # NOQA
    import display_driver_framework

import _indev_base

class EncoderDriver(_indev_base.IndevBase):
    _last_enc_value: int = ...
    _last_enc_diff: int = ...
    _last_key: int = ...

    def __init__(self):
        """
        初始化编码器驱动
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def _get_enc(
        self
    ) -> Optional[Union[Tuple[int, int], Tuple[None, int], Tuple[int, None]]]:
        """
        读取编码器位置和可能存在的按钮
        
        此函数需要返回编码器值和按键值。
        如果其中任何一个没有被使用,则可以返回None。
        如果两个都没有被使用,则返回单个None。
        
        参数:
            无
        返回:
            (Optional[Union[Tuple[int, int], Tuple[None, int], Tuple[int, None]]]): 如果没有按钮按下且没有编码器值则返回None
            
        异常:
            NotImplimentedError: 如果编码器驱动中没有重写此方法
        """
        ...

    def get_scroll_obj(self):
        """
        获取滚动对象
        
        参数:
            无
        返回:
            (object): 滚动对象
        """
        ...

    def get_scroll_dir(self):
        """
        获取滚动方向
        
        参数:
            无
        返回:
            (int): 滚动方向
        """
        ...

    def reset_long_press(self):
        """
        重置长按
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...
