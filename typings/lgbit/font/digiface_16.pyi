"""
数字字体digiface,高度16像素.

由font-to-py.py工具从digiface.ttf转换生成的字体模块.
提供了显示数字和基本字符的点阵字体.
"""

from typing import Tuple, Any

# 字体版本
version: str = '0.26'

def height() -> int:
    """
    获取字体高度.
    
    返回:
        int: 字体高度(像素),固定为16
    """
    ...

def max_width() -> int:
    """
    获取字体最大宽度.
    
    返回:
        int: 字体最大宽度(像素),固定为15
    """
    ...

def hmap() -> bool:
    """
    判断是否为水平映射模式.
    
    返回:
        bool: True表示水平映射,False表示垂直映射
    """
    ...

def reverse() -> bool:
    """
    判断是否为反转模式.
    
    返回:
        bool: True表示反转,False表示正常
    """
    ...

def monospaced() -> bool:
    """
    判断是否为等宽字体.
    
    返回:
        bool: True表示等宽字体,False表示变宽字体
    """
    ...

def min_ch() -> int:
    """
    获取字体支持的最小ASCII码值.
    
    返回:
        int: 最小ASCII码值,固定为32(空格)
    """
    ...

def max_ch() -> int:
    """
    获取字体支持的最大ASCII码值.
    
    返回:
        int: 最大ASCII码值,固定为126(~)
    """
    ...

def get_ch(ch: str) -> Tuple[bytes, int, int]:
    """
    获取指定字符的字体数据.
    
    参数:
        ch: str 要获取的字符,必须是单个字符
    
    返回:
        Tuple[bytes,int,int]: 包含(字体数据, 高度, 宽度)的元组
        
    注意:
        如果字符不在支持范围内(32-126),将返回问号(?)的字体数据
    """
    ... 