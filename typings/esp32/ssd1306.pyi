from typing import Optional, Union, List
from machine import I2C, SPI, Pin
import framebuf
from micropython import const

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_IREF_SELECT = const(0xAD)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

class SSD1306(framebuf.FrameBuffer):
    """SSD1306 OLED显示驱动基类"""
    
    width: int
    height: int
    external_vcc: bool
    pages: int
    buffer: bytearray
    
    def __init__(self, width: int, height: int, external_vcc: bool) -> None:
        """
        初始化SSD1306显示驱动
        
        参数:
            width: int 显示屏宽度（像素）
            height: int 显示屏高度（像素）
            external_vcc: bool 是否使用外部VCC
        """
        ...

    def init_display(self) -> None:
        """初始化显示设置"""
        ...

    def poweroff(self) -> None:
        """关闭显示"""
        ...

    def poweron(self) -> None:
        """开启显示"""
        ...

    def contrast(self, contrast: int) -> None:
        """
        设置显示对比度
        
        参数:
            contrast: int 对比度值(0-255)
        """
        ...

    def invert(self, invert: bool) -> None:
        """
        设置显示反转
        
        参数:
            invert: bool True为反转显示,False为正常显示
        """
        ...

    def rotate(self, rotate: bool) -> None:
        """
        设置显示旋转
        
        参数:
            rotate: bool True为旋转显示,False为正常显示
        """
        ...

    def show(self) -> None:
        """更新显示内容"""
        ...
        
    def write_cmd(self, cmd: int) -> None:
        """
        写入命令（抽象方法，需要在子类中实现）
        
        参数:
            cmd: int 命令字节
        """
        ...
        
    def write_data(self, buf: Union[bytes, bytearray]) -> None:
        """
        写入显示数据（抽象方法，需要在子类中实现）
        
        参数:
            buf: bytes|bytearray 数据缓冲区
        """
        ...

class SSD1306_I2C(SSD1306):
    """SSD1306 OLED I2C接口驱动"""
    
    i2c: I2C
    addr: int
    temp: bytearray
    write_list: List[Union[bytes, bytearray]]
    
    def __init__(self, width: int, height: int, i2c: I2C, addr: int = 0x3C, external_vcc: bool = False) -> None:
        """
        初始化SSD1306 I2C显示驱动
        
        参数:
            width: int 显示屏宽度（像素）
            height: int  显示屏高度（像素）
            i2c: I2C I2C总线对象
            addr: int I2C设备地址
            external_vcc: bool是否使用外部VCC
        """
        ...

    def write_cmd(self, cmd: int) -> None:
        """
        写入命令
        
        参数:
            cmd: int 命令字节
        """
        ...

    def write_data(self, buf: Union[bytes, bytearray]) -> None:
        """
        写入显示数据
        
        参数:
            buf: bytes|bytearray 数据缓冲区
        """
        ...

class SSD1306_SPI(SSD1306):
    """SSD1306 OLED SPI接口驱动"""
    
    spi: SPI
    dc: Pin
    res: Pin
    cs: Pin
    rate: int
    buffer: bytearray
    
    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Pin, cs: Pin, external_vcc: bool = False, rate: int = 8000000) -> None:
        """
        初始化SSD1306 SPI显示驱动
        
        参数:
            width: int显示屏宽度(像素）
            height: int 显示屏高度(像素）
            spi: SPI SPI总线对象
            dc: Pin 数据/命令控制引脚
            res: Pin复位引脚
            cs: PIn 片选引脚
            external_vcc: bool是否使用外部VCC
        """
        ...

    def write_cmd(self, cmd: int) -> None:
        """
        写入命令
        
        参数:
            cmd: int 命令字节
        """
        ...

    def write_data(self, buf: Union[bytes, bytearray]) -> None:
        """
        写入显示数据
        
        参数:
            buf: bytes|bytearray 数据缓冲区
        """
        ...