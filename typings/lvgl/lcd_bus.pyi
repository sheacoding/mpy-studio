"""
LCD总线接口模块

本模块提供了与LCD显示器通信的各种总线接口实现, 包括SPI, I2C, I80和RGB等.
"""

from typing import Any, Callable, Optional, Union, ClassVar, List
from typing_extensions import Final
from builtins import bool, int, bytes, bytearray, memoryview, list
import array
import machine

# 类型别名简化定义
_BufferType = Union[bytearray, memoryview, bytes, array.array]

# 内存类型常量
MEMORY_32BIT: Final[int] = ...
MEMORY_8BIT: Final[int] = ...
MEMORY_DMA: Final[int] = ...
MEMORY_SPIRAM: Final[int] = ...
MEMORY_INTERNAL: Final[int] = ...
MEMORY_DEFAULT: Final[int] = ...
DEBUG_ENABLED: Final[int] = ...


class _LCDBusBase:
    """LCD总线基类, 提供所有总线接口共有的方法"""
    
    def init(
        self, width: int, height: int, bpp: int, buffer_size: int,
        rgb565_byte_swap: bool, cmd_bits: int, param_bits: int
    ) -> None:
        """
        初始化LCD总线
        
        参数:
            width (int): 显示宽度
            height (int): 显示高度
            bpp (int): 每像素位数
            buffer_size (int): 缓冲区大小
            rgb565_byte_swap (bool): RGB565字节交换标志
            cmd_bits (int): 命令位宽
            param_bits (int): 参数位宽
        返回:
            (None): 无返回值
        """
        ...
    
    def deinit(self) -> None:
        """
        释放LCD总线资源
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...
    
    def __del__(self) -> None:
        """
        析构函数, 调用deinit
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...
    
    def register_callback(self, callback: Callable) -> None:
        """
        注册回调函数
        
        参数:
            callback (Callable): 回调函数
        返回:
            (None): 无返回值
        """
        ...
    
    def tx_param(self, cmd: int, params: Optional[_BufferType] = None) -> None:
        """
        发送命令和参数
        
        参数:
            cmd (int): 命令代码
            params (Optional[_BufferType]): 参数数据,默认None
        返回:
            (None): 无返回值
        """
        ...
    
    def tx_color(self, cmd: int, data: _BufferType, x_start: int, y_start: int, 
                x_end: int, y_end: int, rotation: int = 0, last_update: bool = False) -> None:
        """
        发送颜色数据
        
        参数:
            cmd (int): 命令代码
            data (_BufferType): 颜色数据
            x_start (int): 起始X坐标
            y_start (int): 起始Y坐标
            x_end (int): 结束X坐标
            y_end (int): 结束Y坐标
            rotation (int): 旋转角度,默认0
            last_update (bool): 是否为最后一次更新,默认False
        返回:
            (None): 无返回值
        """
        ...
    
    def rx_param(self, cmd: int, data: _BufferType) -> None:
        """
        接收参数
        
        参数:
            cmd (int): 命令代码
            data (_BufferType): 用于存储接收数据的缓冲区
        返回:
            (None): 无返回值
        """
        ...
    
    def get_lane_count(self) -> int:
        """
        获取通道数
        
        参数:
            无
        返回:
            (int): 通道数
        """
        ...
    
    def allocate_framebuffer(self, size: int, caps: int) -> Optional[memoryview]:
        """
        分配帧缓冲区
        
        参数:
            size (int): 缓冲区大小
            caps (int): 内存能力标志
            
        返回:
            (Optional[memoryview]): 分配的帧缓冲区, 如果分配失败则返回None
        """
        ...
    
    def free_framebuffer(self, framebuffer: memoryview) -> None:
        """
        释放帧缓冲区
        
        参数:
            framebuffer (memoryview): 要释放的帧缓冲区
        返回:
            (None): 无返回值
        """
        ...


class I2CBus(_LCDBusBase):
    """I2C总线接口"""

    def __init__(
        self,
        *,
        sda: int,
        scl: int,
        addr: int,
        host: int = 0,
        control_phase_bytes: int = 1,
        dc_bit_offset: int = 6,
        freq: int = 10000000,
        dc_low_on_data: bool = False,
        sda_pullup: bool = True,
        scl_pullup: bool = True,
        disable_control_phase: bool = False
    ):
        """
        初始化I2C总线接口
        
        参数:
            sda (int): SDA引脚
            scl (int): SCL引脚
            addr (int): I2C地址
            host (int): I2C主机号,默认0
            control_phase_bytes (int): 控制阶段字节数,默认1
            dc_bit_offset (int): DC位偏移,默认6
            freq (int): 频率,默认10000000
            dc_low_on_data (bool): 数据时DC为低电平,默认False
            sda_pullup (bool): SDA上拉使能,默认True
            scl_pullup (bool): SCL上拉使能,默认True
            disable_control_phase (bool): 禁用控制阶段,默认False
        返回:
            (None): 无返回值
        """
        ...


class SPIBus(_LCDBusBase):
    """SPI总线接口"""

    def __init__(
        self,
        *,
        spi_bus: machine.SPI.Bus | machine.SPI.DualBus | machine.SPI.QuadBus | machine.SPI.OctalBus,
        dc: int,
        freq: int,
        cs: int = -1,
        dc_low_on_data: bool = False,
        lsb_first: bool = False,
        cs_high_active: bool = False,
        spi_mode: int = 0,
        dual: bool = False,
        quad: bool = False,
        octal: bool = False
    ):
        """
        初始化SPI总线接口
        
        参数:
            spi_bus (machine.SPI.Bus | machine.SPI.DualBus | machine.SPI.QuadBus | machine.SPI.OctalBus): SPI总线对象
            dc (int): DC引脚
            freq (int): 频率
            cs (int): CS引脚, -1表示不使用,默认-1
            dc_low_on_data (bool): 数据时DC为低电平,默认False
            lsb_first (bool): LSB优先,默认False
            cs_high_active (bool): CS高电平有效,默认False
            spi_mode (int): SPI模式,默认0
            dual (bool): 双线模式,默认False
            quad (bool): 四线模式,默认False
            octal (bool): 八线模式,默认False
        返回:
            (None): 无返回值
        """
        ...


class RGBBus(_LCDBusBase):
    """RGB并行总线接口"""

    def __init__(
        self,
        *,
        hsync: int,
        vsync: int,
        de: int,
        pclk: int,
        data0: int,
        data1: int,
        data2: int,
        data3: int,
        data4: int,
        data5: int,
        data6: int,
        data7: int,
        data8: int = -1,
        data9: int = -1,
        data10: int = -1,
        data11: int = -1,
        data12: int = -1,
        data13: int = -1,
        data14: int = -1,
        data15: int = -1,
        freq: int = 8000000,
        hsync_front_porch: int = 0,
        hsync_back_porch: int = 0,
        hsync_pulse_width: int = 1,
        hsync_idle_low: bool = False,
        vsync_front_porch: int = 0,
        vsync_back_porch: int = 0,
        vsync_pulse_width: int = 1,
        vsync_idle_low: bool = False,
        de_idle_high: bool = False,
        pclk_idle_high: bool = False,
        pclk_active_low: bool = False,
        disp_active_low: bool = False,
        refresh_on_demand: bool = False,
        rgb565_dither: bool = False
    ):
        """
        初始化RGB并行总线接口
        
        参数:
            hsync (int): 水平同步信号引脚
            vsync (int): 垂直同步信号引脚
            de (int): 数据使能引脚
            pclk (int): 像素时钟引脚
            data0-data15 (int): 数据引脚
            freq (int): 频率,默认8000000
            hsync_front_porch (int): 水平前肩,默认0
            hsync_back_porch (int): 水平后肩,默认0
            hsync_pulse_width (int): 水平脉冲宽度,默认1
            hsync_idle_low (bool): 水平同步信号空闲时为低电平,默认False
            vsync_front_porch (int): 垂直前肩,默认0
            vsync_back_porch (int): 垂直后肩,默认0
            vsync_pulse_width (int): 垂直脉冲宽度,默认1
            vsync_idle_low (bool): 垂直同步信号空闲时为低电平,默认False
            de_idle_high (bool): 数据使能信号空闲时为高电平,默认False
            pclk_idle_high (bool): 像素时钟空闲时为高电平,默认False
            pclk_active_low (bool): 像素时钟有效时为低电平,默认False
            disp_active_low (bool): 显示有效时为低电平,默认False
            refresh_on_demand (bool): 按需刷新,默认False
            rgb565_dither (bool): RGB565抖动,默认False
        返回:
            (None): 无返回值
        """
        ...


class I80Bus(_LCDBusBase):
    """Intel 8080并行总线接口"""

    def __init__(
        self,
        *,
        dc: int,
        wr: int,
        data0: int,
        data1: int,
        data2: int,
        data3: int,
        data4: int,
        data5: int,
        data6: int,
        data7: int,
        data8: int = -1,
        data9: int = -1,
        data10: int = -1,
        data11: int = -1,
        data12: int = -1,
        data13: int = -1,
        data14: int = -1,
        data15: int = -1,
        cs: int = -1,
        freq: int = 10000000,
        dc_idle_high: bool = False,
        dc_cmd_high: bool = False,
        dc_dummy_high: bool = False,
        dc_data_high: bool = True,
        cs_active_high: bool = False,
        reverse_color_bits: bool = False,
        swap_color_bytes: bool = False,
        pclk_active_low: bool = False,
        pclk_idle_low: bool = False,
    ):
        """
        初始化Intel 8080并行总线接口
        
        参数:
            dc (int): 数据/命令选择引脚
            wr (int): 写使能引脚
            data0-data15 (int): 数据引脚
            cs (int): 片选引脚, -1表示不使用,默认-1
            freq (int): 频率,默认10000000
            dc_idle_high (bool): DC空闲时为高电平,默认False
            dc_cmd_high (bool): 命令时DC为高电平,默认False
            dc_dummy_high (bool): 空操作时DC为高电平,默认False
            dc_data_high (bool): 数据时DC为高电平,默认True
            cs_active_high (bool): CS高电平有效,默认False
            reverse_color_bits (bool): 反转颜色位,默认False
            swap_color_bytes (bool): 交换颜色字节,默认False
            pclk_active_low (bool): 时钟有效时为低电平,默认False
            pclk_idle_low (bool): 时钟空闲时为低电平,默认False
        返回:
            (None): 无返回值
        """
        ...


# 仅在UNIX平台可用
class SDLBus(_LCDBusBase):
    """SDL模拟总线接口, 仅在UNIX平台可用"""
    
    # 窗口标志常量
    WINDOW_FULLSCREEN: ClassVar[int] = ...
    WINDOW_FULLSCREEN_DESKTOP: ClassVar[int] = ...
    WINDOW_BORDERLESS: ClassVar[int] = ...
    WINDOW_MINIMIZED: ClassVar[int] = ...
    WINDOW_MAXIMIZED: ClassVar[int] = ...
    WINDOW_ALLOW_HIGHDPI: ClassVar[int] = ...
    WINDOW_ALWAYS_ON_TOP: ClassVar[int] = ...
    WINDOW_SKIP_TASKBAR: ClassVar[int] = ...
    WINDOW_UTILITY: ClassVar[int] = ...
    WINDOW_TOOLTIP: ClassVar[int] = ...
    WINDOW_POPUP_MENU: ClassVar[int] = ...

    def __init__(
        self,
        *,
        flags: int
    ):
        """
        初始化SDL模拟总线接口
        
        参数:
            flags (int): 窗口标志
        返回:
            (None): 无返回值
        """
        ...

    def register_mouse_callback(
        self,
        callback: Callable[[list], None],
    ) -> None:
        """
        注册鼠标事件回调函数
        
        参数:
            callback (Callable[[list], None]): 回调函数
        返回:
            (None): 无返回值
        """
        ...

    def register_window_callback(
        self,
        callback: Callable[[list], None],
    ) -> None:
        """
        注册窗口事件回调函数
        
        参数:
            callback (Callable[[list], None]): 回调函数
        返回:
            (None): 无返回值
        """
        ...

    def register_keypad_callback(
        self,
        callback: Callable[[list], None],
    ) -> None:
        """
        注册键盘事件回调函数
        
        参数:
            callback (Callable[[list], None]): 回调函数
        返回:
            (None): 无返回值
        """
        ...

    def register_quit_callback(
        self,
        callback: Callable[[], None],
    ) -> None:
        """
        注册退出事件回调函数
        
        参数:
            callback (Callable[[], None]): 回调函数
        返回:
            (None): 无返回值
        """
        ...

    def set_window_size(
        self,
        width: int,
        height: int,
        px_format: int,
        ignore_size_chg: bool,
    ) -> None:
        """
        设置窗口大小
        
        参数:
            width (int): 宽度
            height (int): 高度
            px_format (int): 像素格式
            ignore_size_chg (bool): 忽略大小变化
        返回:
            (None): 无返回值
        """
        ...

    def poll_events(self) -> None:
        """
        轮询SDL事件
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...


def _pump_main_thread() -> None:
    """
    处理主线程中的待处理事件
    
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...


# 清理导入的类型, 不暴露给用户
del Any
del Callable
del Optional
del Union
del array
del _BufferType
