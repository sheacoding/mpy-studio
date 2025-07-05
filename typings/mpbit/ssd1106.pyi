# ssd1106.pyi

from typing import Union, Optional, Any
import framebuf
import micropython

# 常量定义.
SET_CONTRAST: int
SET_ENTIRE_ON: int
SET_ENTIRE_ON1: int
SET_NORM_INV: int
SET_DISP_OFF: int
SET_DISP_ON: int
SET_MEM_ADDR: int
SET_COL_ADDR: int
SET_PAGE_ADDR: int
SET_DISP_START_LINE: int
SET_SEG_REMAP: int
SET_MUX_RATIO: int
SET_COM_OUT_DIR: int
SET_DISP_OFFSET: int
SET_COM_PIN_CFG: int
SET_DISP_CLK_DIV: int
SET_PRECHARGE: int
SET_VCOM_DESEL: int
SET_CHARGE_PUMP: int
SET_CHARGE_PUMP1: int
SET_COL_ADDR_L: int
SET_COL_ADDR_H: int
SET_PAGE_ADDR1: int
SET_CONTRACT_CTRL: int
SET_DUTY: int
SET_VCC_SOURCE: int
SET_VPP: int


class SSD1106(framebuf.FrameBuffer):
    """
    SSD1106 OLED 显示屏驱动基类.
    
    参数:
        width (int): 屏幕宽度(如 128).
        height (int): 屏幕高度(如 64 或 32).
        external_vcc (bool): 是否使用外部 VCC 电源.
    """

    def __init__(self, width: int, height: int, external_vcc: bool) -> None: ...

    def write_cmd(self, cmd: int) -> None:
        """
        向显示屏写入命令.需要子类实现.
        
        参数:
            cmd (int): 要写入的命令字节.
        """
        ...

    def write_data(self, buf: bytearray) -> None:
        """
        向显示屏写入数据.需要子类实现.
        
        参数:
            buf (bytearray): 数据缓冲区.
        """
        ...

    def init_display(self) -> None:
        """
        初始化显示屏配置.
        """
        ...

    def poweroff(self) -> None:
        """
        关闭显示屏电源.
        """
        ...

    def poweron(self) -> None:
        """
        打开显示屏电源.
        """
        ...

    def contrast(self, contrast: int) -> None:
        """
        设置显示对比度.
        
        参数:
            contrast (int): 对比度值(0x00 到 0xFF).
        """
        ...

    def invert(self, invert: bool) -> None:
        """
        设置是否反色显示.
        
        参数:
            invert (bool): True 表示反色,False 表示正常显示.
        """
        ...

    def show(self) -> None:
        """
        将帧缓冲区的内容刷新到物理屏幕.
        """
        ...


class SSD1106_I2C(SSD1106):
    """
    使用 I2C 接口的 SSD1106 OLED 驱动.
    
    参数:
        width (int): 屏幕宽度.
        height (int): 屏幕高度.
        i2c: I2C 总线对象.
        addr (int): I2C 地址,默认为 0x3c.
        external_vcc (bool): 是否使用外部 VCC.
    """

    def __init__(
        self,
        width: int,
        height: int,
        i2c: Any,
        addr: int = 0x3c,
        external_vcc: bool = False
    ) -> None:
        ...

    def write_cmd(self, cmd: int) -> None:
        """
        向 SSD1106 写入命令(I2C 接口).
        
        参数:
            cmd (int): 命令字节.
        """
        ...

    def write_data(self, buf: bytearray) -> None:
        """
        向 SSD1106 写入数据(I2C 接口).
        
        参数:
            buf (bytearray): 数据缓冲区.
        """
        ...


class SSD1106_SPI(SSD1106):
    """
    使用 SPI 接口的 SSD1106 OLED 驱动.
    
    参数:
        width (int): 屏幕宽度.
        height (int): 屏幕高度.
        spi: SPI 总线对象.
        dc: 数据/命令选择引脚.
        res: 复位引脚.
        cs: 片选引脚.
        external_vcc (bool): 是否使用外部 VCC.
    """

    def __init__(
        self,
        width: int,
        height: int,
        spi: Any,
        dc: Any,
        res: Any,
        cs: Any,
        external_vcc: bool = False
    ) -> None:
        ...

    def write_cmd(self, cmd: int) -> None:
        """
        向 SSD1106 写入命令(SPI 接口).
        
        参数:
            cmd (int): 命令字节.
        """
        ...

    def write_data(self, buf: bytearray) -> None:
        """
        向 SSD1106 写入数据(SPI 接口).
        
        参数:
            buf (bytearray): 数据缓冲区.
        """
        ...