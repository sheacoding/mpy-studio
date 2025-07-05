# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, Tuple, Union, ClassVar, Callable, List, Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import micropython  # NOQA
    import machine  # NOQA
    import lvgl as lv  # NOQA
    import array  # NOQA
    import io_expander_framework  # NOQA

import lcd_bus


# Constants

BYTE_ORDER_RGB: int = ...
BYTE_ORDER_BGR: int = ...

STATE_HIGH: int = ...
STATE_LOW: int = ...
STATE_PWM: int = ...

_BufferType = Union[bytearray, memoryview, bytes, array.array]
_PinType = Union[machine.Pin, int, io_expander_framework.Pin]
_DatabusType = Union[lcd_bus.I80Bus, lcd_bus.I2CBus, lcd_bus.RGBBus, lcd_bus.SPIBus, lcd_bus.SDLBus]


class DisplayDriver:
    _INVON: ClassVar[int] = ...
    _INVOFF: ClassVar[int] = ...

    # MADCTL values for each of the orientation constants for non-st7789 displays.
    _ORIENTATION_TABLE: ClassVar[Tuple[int, int, int, int]] = ...

    _displays: ClassVar[list[_DatabusType]] = ...

    display_width: int = ...
    display_height: int = ...
    _reset_pin: Optional[_PinType] = ...
    _reset_state: int = ...
    _power_pin: Optional[_PinType] = ...
    _power_on_state: int = ...
    _backlight_pin: Optional[_PinType] = ...
    _backlight_on_state: int = ...
    _offset_x: int = ...
    _offset_y: int = ...
    _data_bus: _DatabusType = ...
    _param_buf: bytearray = ...
    _param_mv: memoryview = ...
    _disp_drv: lv.display_driver_t = ...  # NOQA
    _color_byte_order: int = ...
    _color_space: int = ...
    _physical_width: int = ...
    _physical_height: int = ...
    _initilized: bool = ...
    _frame_buffer1: Optional[_BufferType] = ...
    _frame_buffer2: Optional[_BufferType] = ...
    _backup_set_memory_location: Optional[Callable] = ...
    _rotation: int = ...
    _spi_3wire: lcd_bus.SPI3Wire = None

    # Default values of "power" and "backlight" are reversed logic! 0 means ON.
    # You can change this by setting backlight_on and power_on arguments.
    #
    # For the ESP32 the allocation of the frame buffers can be done one of 2
    # ways depending on what is wanted in terms of performance VS memory use
    # If a single frame buffer is used then using a DMA transfer is pointless
    # to do. The frame buffer in this casse can be allocated as simple as
    #
    # buf = bytearray(buffer_size)
    #
    # If the user wants to be able to specify if the frame buffer is to be
    # created in internal memory (SRAM) or in external memory (PSRAM/SPIRAM)
    # this can be done using the heap_caps module.
    #
    # internal memory:
    # buf = heap_caps.malloc(buffer_size, heap_caps.CAP_INTERNAL)
    #
    # external memory:
    # buf = heap_caps.malloc(buffer_size, heap_caps.CAP_SPIRAM)
    #
    # If wanting to use DMA memory then use the bitwise OR "|" operator to add
    # the DMA flag to the last parameter of the malloc function
    #
    # buf = heap_caps.malloc(
    #     buffer_size, heap_caps.CAP_INTERNAL | heap_caps.CAP_DMA
    # )

    @staticmethod
    def get_default() -> "DisplayDriver":
        """
        获取默认显示驱动
        
        参数:
            无
        返回:
            (DisplayDriver): 默认显示驱动对象
        """
        ...

    @staticmethod
    def get_displays() -> List["DisplayDriver"]:
        """
        获取所有显示驱动列表
        
        参数:
            无
        返回:
            (List[DisplayDriver]): 显示驱动对象列表
        """
        ...

    def __init__(
        self,
        data_bus: _DatabusType,
        display_width: int,
        display_height: int,
        frame_buffer1: Optional[_BufferType] = None,
        frame_buffer2: Optional[_BufferType] = None,
        reset_pin: Optional[_PinType] = None,
        reset_state: int = STATE_HIGH,
        power_pin: Optional[_PinType] = None,
        power_on_state: int = STATE_HIGH,
        backlight_pin: Optional[_PinType] = None,
        backlight_on_state: int = STATE_HIGH,
        offset_x: int = 0,
        offset_y: int = 0,
        color_byte_order: int = BYTE_ORDER_RGB,
        color_space: int = lv.COLOR_FORMAT.RGB888,  # NOQA
        rgb565_byte_swap: bool = False,
        spi_3wire: Optional[lcd_bus.SPI3Wire] = None,
        _cmd_bits: int = 8,
        _param_bits: int = 8,
        _init_bus: bool = True
    ) -> object:
        """
        初始化显示驱动
        
        参数:
            data_bus (_DatabusType): 数据总线对象
            display_width (int): 显示宽度
            display_height (int): 显示高度
            frame_buffer1 (Optional[_BufferType]): 帧缓冲区1，默认None
            frame_buffer2 (Optional[_BufferType]): 帧缓冲区2，默认None
            reset_pin (Optional[_PinType]): 复位引脚，默认None
            reset_state (int): 复位状态，默认STATE_HIGH
            power_pin (Optional[_PinType]): 电源引脚，默认None
            power_on_state (int): 电源开启状态，默认STATE_HIGH
            backlight_pin (Optional[_PinType]): 背光引脚，默认None
            backlight_on_state (int): 背光开启状态，默认STATE_HIGH
            offset_x (int): X轴偏移，默认0
            offset_y (int): Y轴偏移，默认0
            color_byte_order (int): 颜色字节顺序，默认BYTE_ORDER_RGB
            color_space (int): 颜色空间，默认RGB888
            rgb565_byte_swap (bool): RGB565字节交换，默认False
            spi_3wire (Optional[lcd_bus.SPI3Wire]): 3线SPI，默认None
            _cmd_bits (int): 命令位数，默认8
            _param_bits (int): 参数位数，默认8
            _init_bus (bool): 是否初始化总线，默认True
        返回:
            (object): 显示驱动对象
        """
        ...

    def set_physical_resolution(self, width: int, height: int) -> None:
        """
        设置物理分辨率
        
        参数:
            width (int): 物理宽度
            height (int): 物理高度
        返回:
            (None): 无返回值
        """
        ...

    def get_physical_horizontal_resolution(self) -> int:
        """
        获取物理水平分辨率
        
        参数:
            无
        返回:
            (int): 物理水平分辨率
        """
        ...

    def get_physical_vertical_resolution(self) -> int:
        """
        获取物理垂直分辨率
        
        参数:
            无
        返回:
            (int): 物理垂直分辨率
        """
        ...

    def set_physical_horizontal_resolution(self, width: int) -> None:
        """
        设置物理水平分辨率
        
        参数:
            width (int): 物理宽度
        返回:
            (None): 无返回值
        """
        ...

    def set_physical_vertical_resolution(self, height: int) -> None:
        """
        设置物理垂直分辨率
        
        参数:
            height (int): 物理高度
        返回:
            (None): 无返回值
        """
        ...

    def get_next(self) -> "DisplayDriver":
        """
        获取下一个显示驱动
        
        参数:
            无
        返回:
            (DisplayDriver): 下一个显示驱动对象
        """
        ...

    def set_offset(self, x: int, y: int) -> None:
        """
        设置偏移量
        
        参数:
            x (int): X轴偏移
            y (int): Y轴偏移
        返回:
            (None): 无返回值
        """
        ...

    def get_offset_x(self) -> int:
        """
        获取X轴偏移
        
        参数:
            无
        返回:
            (int): X轴偏移值
        """
        ...

    def get_offset_y(self) -> int:
        """
        获取Y轴偏移
        
        参数:
            无
        返回:
            (int): Y轴偏移值
        """
        ...

    def get_dpi(self) -> int:
        """
        获取DPI值
        
        参数:
            无
        返回:
            (int): DPI值
        """
        ...

    def set_dpi(self, dpi: int) -> None:
        """
        设置DPI值
        
        参数:
            dpi (int): DPI值
        返回:
            (None): 无返回值
        """
        ...

    def set_color_format(self, color_space: int) -> None:
        """
        设置颜色格式
        
        参数:
            color_space (int): 颜色空间
        返回:
            (None): 无返回值
        """
        ...

    def get_color_format(self) -> int:
        """
        获取颜色格式
        
        参数:
            无
        返回:
            (int): 颜色格式
        """
        ...

    def set_antialiasing(self, en: bool) -> None:
        """
        设置抗锯齿
        
        参数:
            en (bool): 是否启用抗锯齿
        返回:
            (None): 无返回值
        """
        ...

    def get_antialiasing(self) -> bool:
        """
        获取抗锯齿状态
        
        参数:
            无
        返回:
            (bool): 抗锯齿状态
        """
        ...

    def is_double_buffered(self) -> bool:
        """
        检查是否双缓冲
        
        参数:
            无
        返回:
            (bool): 是否双缓冲
        """
        ...

    def get_screen_active(self) -> lv.obj:  # NOQA
        """
        获取活动屏幕
        
        参数:
            无
        返回:
            (lv.obj): 活动屏幕对象
        """
        ...

    def get_screen_prev(self) -> lv.obj:  # NOQA
        """
        获取上一个屏幕
        
        参数:
            无
        返回:
            (lv.obj): 上一个屏幕对象
        """
        ...

    def get_layer_top(self) -> lv.obj:  # NOQA
        """
        获取顶层图层
        
        参数:
            无
        返回:
            (lv.obj): 顶层图层对象
        """
        ...

    def get_layer_sys(self) -> lv.obj:  # NOQA
        """
        获取系统图层
        
        参数:
            无
        返回:
            (lv.obj): 系统图层对象
        """
        ...

    def get_layer_bottom(self) -> lv.obj:  # NOQA
        """
        获取底层图层
        
        参数:
            无
        返回:
            (lv.obj): 底层图层对象
        """
        ...

    def add_event_cb(self, event_cb, filter, user_data) -> None:  # NOQA
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

    def get_event_count(self) -> int:
        """
        获取事件数量
        
        参数:
            无
        返回:
            (int): 事件数量
        """
        ...

    def get_event_dsc(self, index: int) -> lv.event_dsc_t:
        """
        获取事件描述符
        
        参数:
            index (int): 事件索引
        返回:
            (lv.event_dsc_t): 事件描述符
        """
        ...

    def delete_event(self, index: int) -> bool:
        """
        删除事件
        
        参数:
            index (int): 事件索引
        返回:
            (bool): 删除是否成功
        """
        ...

    def send_event(self, code: int, param: Any) -> int:
        """
        发送事件
        
        参数:
            code (int): 事件代码
            param (Any): 事件参数
        返回:
            (int): 发送结果
        """
        ...

    def set_theme(self, th: lv.theme_t) -> None:
        ...

    def get_theme(self) -> lv.theme_t:
        ...

    def get_inactive_time(self) -> int:
        ...

    def trigger_activity(self) -> None:
        ...

    def enable_invalidation(self, en: bool) -> None:
        ...

    def is_invalidation_enabled(self) -> bool:
        ...

    def get_refr_timer(self) -> lv.timer_t:
        ...

    def delete_refr_timer(self) -> None:
        ...

    def invert_colors(self) -> None:
        ...

    def set_default(self) -> None:
        ...

    def get_rotation(self) -> int:
        ...

    def set_rotation(self, value: int) -> None:
        ...

    def get_horizontal_resolution(self) -> int:
        ...

    def get_vertical_resolution(self) -> int:
        ...

    def init(self) -> None:
        ...

    def set_params(self, cmd: int, params: Optional[_BufferType] = None) -> None:
        ...

    def get_params(self, cmd: int, params: _BufferType) -> None:
        ...

    def get_power(self) -> bool:
        ...

    def set_power(self, value: bool) -> None:
        ...

    def delete(self) -> None:
        ...

    def __del__(self):
        ...

    def reset(self) -> None:
        ...

    def get_backlight(self) -> Union[int, float]:
        ...

    def set_backlight(self, value: Union[int, float]) -> None:
        ...

    def _dummy_set_memory_location(self, *_, **__) -> int:  # NOQA
        ...

    # this function is handeled in the viper code emitter. This will
    # increase the performance to near C code execution times. While this is
    # not really heavy lifting in terms of work being done every cycle counts
    # and it adds up over time. Need to keep things running as fast as possible.

    def _set_memory_location(self, x1: int, y1: int, x2: int, y2: int) -> int:
        ...

    def _flush_cb(self, disp: lv.display_driver_t, area: lv.area_t, color_p: lv.CArray) -> None:  # NOQA
        ...

    # we always register this callback no matter what. This is what tells LVGL
    # that the buffer is able to be written to. If this callback doesn't get
    # registered then the flush function is going to block until the buffer
    # gets emptied. Everything is handeled internally in the bus driver if
    # using DMA and double buffer or a single buffer.

    def _flush_ready_cb(self, *param) -> None:
        ...

    def _madctl(self, colormode: int, rotations: Tuple[int, int, int, int], rotation: Optional[int] = None) -> int:
        ...

    def deinit(self) -> None:
        ...
