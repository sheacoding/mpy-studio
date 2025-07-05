# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, TYPE_CHECKING

import _indev_base

if TYPE_CHECKING:
    import lvgl as _lv


class ButtonDriver(_indev_base.IndevBase):
    _last_button: int = ...

    def set_button_points(self, *points: list[_lv.point_t]) -> None:
        """
        设置按钮点
        
        参数:
            *points (list[_lv.point_t]): 可变参数，按钮点列表
                使用示例:
                
                button_driver.set_button_points(
                    (lv.point_t(dict(x=0, y=0)), lv.point_t(dict(x=100, y=50))),
                    (lv.point_t(dict(x=0, y=55)), lv.point_t(dict(x=100, y=110))),
                    (lv.point_t(dict(x=0, y=115)), lv.point_t(dict(x=100, y=170)))
                )
                
                您不需要担心保持对点的引用，这在驱动内部完成。
                但是您需要保持对驱动的引用。
        返回:
            (None): 无返回值
        """

    def __init__(self):
        """
        初始化按钮驱动
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def _get_button(self) -> Optional[int]:
        """
        读取按钮状态
        
        此函数需要返回被按下按钮的ID。
        为了使此功能正常工作，您需要将点添加到相应的软件按钮中。
        ID将是您设置的点的索引号。
        
        参数:
            无
        返回:
            (Optional[int]): 如果没有按钮被按下则返回None，否则返回按钮ID
            
        异常:
            NotImplimentedError: 如果按钮驱动中没有重写此方法
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
