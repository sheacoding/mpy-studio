# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional

class Spi3Wire:

    def __init__(
        self,
        scl: int,
        sda: int,
        cs: int,
        freq: int,
        spi_mode: int = 0,
        use_dc_bit: bool = True,
        dc_zero_on_data: bool = False,
        lsb_first: bool = False,
        cs_high_active: bool = False,
        del_keep_cs_inactive: bool = False,
    ):
        """
        初始化3线SPI接口
        
        参数:
            scl (int): SCL引脚
            sda (int): SDA引脚
            cs (int): CS引脚
            freq (int): 频率
            spi_mode (int): SPI模式，默认0
            use_dc_bit (bool): 是否使用DC位，默认True
            dc_zero_on_data (bool): 数据时DC为0，默认False
            lsb_first (bool): LSB优先，默认False
            cs_high_active (bool): CS高电平有效，默认False
            del_keep_cs_inactive (bool): 延迟保持CS无效，默认False
        返回:
            (None): 无返回值
        """
        ...

    def __del__(self):
        """
        析构函数
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def init(self, cmd_bits: int, param_bits: int) -> None:
        """
        初始化SPI接口
        
        参数:
            cmd_bits (int): 命令位数
            param_bits (int): 参数位数
        返回:
            (None): 无返回值
        """
        ...

    def deinit(self) -> None:
        """
        反初始化SPI接口
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def tx_param(self, cmd: int, params: Optional[memoryview]=None):
        """
        发送参数
        
        参数:
            cmd (int): 命令
            params (Optional[memoryview]): 参数，默认None
        返回:
            (None): 无返回值
        """
        ...
