# rgb_display_framework.pyi

import lvgl as lv
import display_driver_framework

class RGBDisplayDriver(display_driver_framework.DisplayDriver):
    '''RGB 显示驱动类'''

    def __init__(
        self,
        data_bus,
        display_width: int,
        display_height: int,
        frame_buffer1 = ...,  # 可选
        frame_buffer2 = ...,  # 可选
        reset_pin = ...,      # 可选
        reset_state: int = ...,  # 可选
        power_pin = ...,      # 可选
        power_on_state: int = ...,  # 可选
        backlight_pin = ...,  # 可选
        backlight_on_state: int = ...,  # 可选
        offset_x: int = 0,
        offset_y: int = 0,
        color_byte_order: int = ...,  # 可选
        color_space = ...,   # 可选
        rgb565_byte_swap: bool = False,
        spi_3wire = ...,    # 可选
        spi_3wire_shared_pins: bool = False,
        _cmd_bits: int = 8,
        _param_bits: int = 8,
        _init_bus: bool = True
    ) -> None:
        '''
        构造函数
        参数:
            data_bus: 数据总线对象
            display_width (int): 显示宽度
            display_height (int): 显示高度
            frame_buffer1: 帧缓冲区1
            frame_buffer2: 帧缓冲区2
            reset_pin: 复位引脚
            reset_state (int): 复位有效电平
            power_pin: 电源引脚
            power_on_state (int): 电源有效电平
            backlight_pin: 背光引脚
            backlight_on_state (int): 背光有效电平
            offset_x (int): X 偏移
            offset_y (int): Y 偏移
            color_byte_order (int): 色彩字节序
            color_space: 色彩空间
            rgb565_byte_swap (bool): 是否交换 RGB565 字节序
            spi_3wire: SPI 3 线对象
            spi_3wire_shared_pins (bool): SPI 3 线是否共用引脚
            _cmd_bits (int): 命令位宽
            _param_bits (int): 参数位宽
            _init_bus (bool): 是否初始化总线
        返回:
            None: 无返回值
        '''
        ...

    def set_params(self, cmd, params = ...) -> None:
        '''
        设置显示参数
        参数:
            cmd: 命令
            params: 参数
        返回:
            None: 无返回值
        '''
        ...

    def get_params(self, cmd, params) -> None:
        '''
        获取显示参数（未实现)
        参数:
            cmd: 命令
            params: 参数
        返回:
            None: 无返回值
        '''
        ...

    def _set_memory_location(self, x1: int, y1: int, x2: int, y2: int) -> int:
        '''
        设置内存位置（重载,RGB 总线无效)
        参数:
            x1 (int): 起始 X
            y1 (int): 起始 Y
            x2 (int): 结束 X
            y2 (int): 结束 Y
        返回:
            int: 返回 -1
        '''
        ...

    def _spi_3wire_init(self, *args, **kwargs) -> None:
        '''
        SPI 3 线初始化（未实现)
        参数:
            *args: 位置参数
            **kwargs: 关键字参数
        返回:
            None: 无返回值
        '''
        ...

    def init(self, type = ...) -> None:
        '''
        初始化显示驱动
        参数:
            type: 初始化类型
        返回:
            None: 无返回值
        '''
        ... 