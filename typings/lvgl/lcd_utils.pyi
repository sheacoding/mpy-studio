# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Union

def remap(
    value: Union[float, int],
    old_min: Union[float, int],
    old_max: Union[float, int],
    new_min: Union[float, int],
    new_max: Union[float, int]
) -> Union[float, int]:
    """
    将值从一个范围重新映射到另一个范围
    
    注意: 如果任何参数是float类型,则返回值也是float类型。
          如果所有参数都是int类型,则返回值也是int类型。
    
    参数:
        value (Union[float, int]): 要重新映射的值
        old_min (Union[float, int]): 原范围的最小值
        old_max (Union[float, int]): 原范围的最大值
        new_min (Union[float, int]): 新范围的最小值
        new_max (Union[float, int]): 新范围的最大值
    返回:
        (Union[float, int]): 映射到新范围的值
    """
    ...


def int_float_converter(value: Union[float, int], /) -> Union[float, int]:
    """
    整数浮点数转换器
    
    参数:
        value (Union[float, int]): 要转换的值
    返回:
        (Union[float, int]): 转换后的值
    """
    ...


def spi_mode_to_polarity_phase(mode: int, /) -> tuple[int]:
    """
    将SPI模式转换为极性和相位
    
    参数:
        mode (int): SPI模式,可以是0、1、2或3
    返回:
        (tuple[int]): 两个整数值(polarity, phase)
    """
    ...

def spi_polarity_phase_to_mode(polarity: int, phase: int, /) -> int:
    """
    将极性和相位转换为SPI模式
    
    参数:
        polarity (int): 极性,1或0
        phase (int): 相位,1或0
    返回:
        (int): SPI模式,0、1、2或3
    """
    ...