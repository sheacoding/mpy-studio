# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, Tuple, TYPE_CHECKING
import _indev_base
import lcd_utils as _lcd_utils
import lvgl as _lv  # NOQA

lv = _lv


if TYPE_CHECKING:
    import touch_cal_data as _touch_cal_data
    import display_driver_framework as _display_driver_framework



remap = _lcd_utils.remap
_remap = _lcd_utils.remap


class PointerDriver(_indev_base.IndevBase):
    _last_x: int = ...
    _last_y: int = ...
    _orig_width: int = ...
    _orig_height: int = ...
    _config: _touch_cal_data.TouchCalData = ...

    def __init__(self, touch_cal: Optional[_touch_cal_data.TouchCalData] = None, startup_rotation=lv.DISPLAY_ROTATION._0, debug: bool=False):
        """
        初始化指针驱动
        
        参数:
            touch_cal (Optional[_touch_cal_data.TouchCalData]): 触摸校准数据,默认None
            startup_rotation: 启动旋转,默认0度
            debug (bool): 调试模式,默认False
        返回:
            (None): 无返回值
        """
        ...

    def calibrate(self) -> None:
        """
        校准触摸
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    @property
    def is_calibrated(self) -> bool:
        """
        检查是否已校准
        
        参数:
            无
        返回:
            (bool): 是否已校准
        """
        ...

    def _get_coords(self) -> Optional[Tuple[int, int, int]]:
        """
        读取触摸坐标
        
        这是触摸驱动完成工作的地方。当制作触摸驱动时,此方法必须被重写。
        
        参数:
            无
        返回:
            (Optional[Tuple[int, int, int]]): 如果没有触摸输入则返回None,否则返回(x, y)元组
            
        异常:
            NotImplimentedError: 如果触摸驱动中没有重写此方法
        """
        ...

    def get_vect(self, point: lv.point_t):
        """
        获取向量
        
        参数:
            point (lv.point_t): 点对象
        返回:
            (tuple): 向量值
        """
        ...

    def get_scroll_obj(self) -> Optional[lv.obj]:
        """
        获取滚动对象
        
        参数:
            无
        返回:
            (Optional[lv.obj]): 滚动对象
        """
        ...

    def get_scroll_dir(self) -> int:
        """
        获取滚动方向
        
        参数:
            无
        返回:
            (int): 滚动方向
        """
        ...

    def get_gesture_dir(self) -> int:
        """
        获取手势方向
        
        参数:
            无
        返回:
            (int): 手势方向
        """
        ...

    def get_point(self, point: lv.point_t) -> None:
        """
        获取点坐标
        
        参数:
            point (lv.point_t): 点对象
        返回:
            (None): 无返回值
        """
        ...

    def set_cursor(self, cur_obj) -> None:
        """
        设置光标
        
        参数:
            cur_obj: 光标对象
        返回:
            (None): 无返回值
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
