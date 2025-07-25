# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, ClassVar, TYPE_CHECKING, Union


if TYPE_CHECKING:
    import lvgl as _lv  # NOQA
    import display_driver_framework as _display_driver_framework
    from keypad_framework import KeypadDriver as _KeypadDriver
    from pointer_framework import PointerDriver as _PointerDriver
    from encoder_framework import EncoderDriver as _EncoderDriver
    from button_framework import ButtonDriver as _ButtonDriver


class IndevBase:
    _instance_counter: ClassVar[int] = ...
    _indevs: ClassVar[list]

    PRESSED: ClassVar[int] = ...
    RELEASED: ClassVar[int] = ...

    id: int = ...

    _disp_drv: _lv.display_t = ...
    _py_disp_drv: _display_driver_framework.DisplayDriver

    _height: int = ...
    _width: int = ...

    _indev_drv: _lv.indev_t = ...
    _current_state: int = ...

    def __init__(self, debug: bool=False):  # NOQA
        """
        初始化输入设备基类
        
        参数:
            debug (bool): 调试模式,默认False
        返回:
            (None): 无返回值
        """
        ...

    def get_width(self) -> int:
        """
        获取宽度
        
        参数:
            无
        返回:
            (int): 宽度值
        """
        ...

    def get_height(self) -> int:
        """
        获取高度
        
        参数:
            无
        返回:
            (int): 高度值
        """
        ...

    def get_rotation(self) -> int:
        """
        获取旋转角度
        
        参数:
            无
        返回:
            (int): 旋转角度
        """
        ...

    def _read(self, drv, data):  # NOQA
        """
        内部读取方法
        
        参数:
            drv: 驱动对象
            data: 数据对象
        返回:
            (None): 无返回值
        """
        ...

    def read(self):
        """
        读取输入数据
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def get_type(self) -> int:
        """
        获取设备类型
        
        参数:
            无
        返回:
            (int): 设备类型
        """
        ...

    def send_event(self, code: _lv.event_t, param: int) -> bool:
        """
        发送事件
        
        参数:
            code (_lv.event_t): 事件代码
            param (int): 事件参数
        返回:
            (bool): 发送是否成功
        """
        ...

    def remove_event(self, index) -> None:
        """
        移除事件
        
        参数:
            index: 事件索引
        返回:
            (None): 无返回值
        """
        ...

    def get_event_dsc(self, index) -> Optional[_lv.event_dsc_t]:
        """
        获取事件描述符
        
        参数:
            index: 事件索引
        返回:
            (Optional[_lv.event_dsc_t]): 事件描述符
        """
        ...

    def get_event_count(self) -> int:
        """
        获取事件数量
        
        参数:
            无
        返回:
            (int): 事件数量
        """
        ...

    def add_event_cb(self, event_cb, filter, user_data) -> None:
        """
        添加事件回调
        
        参数:
            event_cb: 事件回调函数
            filter: 事件过滤器
            user_data: 用户数据
        返回:
            (None): 无返回值
        """
        ...

    def search_obj(self, point: _lv.point_t) -> Optional[_lv.obj]:
        """
        搜索对象
        
        参数:
            point (_lv.point_t): 点对象
        返回:
            (Optional[_lv.obj]): 找到的对象
        """
        ...

    def delete_read_timer(self) -> None:
        """
        删除读取定时器
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def get_read_timer(self) -> _lv.timer_t:
        """
        获取读取定时器
        
        参数:
            无
        返回:
            (_lv.timer_t): 定时器对象
        """
        ...

    def get_active_obj(self) -> _lv.obj:
        """
        获取活动对象
        
        参数:
            无
        返回:
            (_lv.obj): 活动对象
        """
        ...

    def wait_release(self) -> None:
        """
        等待释放
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def get_state(self):
        """
        获取状态
        
        参数:
            无
        返回:
            (int): 状态值
        """
        ...

    def enable(self, en: bool) -> None:
        """
        启用或禁用设备
        
        参数:
            en (bool): 是否启用
        返回:
            (None): 无返回值
        """
        ...

    def get_group(self):
        """
        获取组
        
        参数:
            无
        返回:
            (object): 组对象
        """
        ...

    def set_group(self, group) -> None:
        """
        设置组
        
        参数:
            group: 组对象
        返回:
            (None): 无返回值
        """
        ...

    def reset(self, obj) -> None:
        """
        重置对象
        
        参数:
            obj: 要重置的对象
        返回:
            (None): 无返回值
        """
        ...

    def get_disp(self) -> _display_driver_framework.DisplayDriver:
        """
        获取显示驱动
        
        参数:
            无
        返回:
            (_display_driver_framework.DisplayDriver): 显示驱动对象
        """
        ...

    @staticmethod
    def active() -> Optional[
        Union[_KeypadDriver, _PointerDriver, _EncoderDriver, _ButtonDriver]
    ]:
        """
        获取活动的输入设备
        
        参数:
            无
        返回:
            (Optional[Union[_KeypadDriver, _PointerDriver, _EncoderDriver, _ButtonDriver]]): 活动的输入设备
        """
        ...
