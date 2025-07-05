"""
JPEG 编解码器模块类型定义
基于 esp-new-jpeg 的 MicroPython 绑定
"""

from typing import Union, Optional, List, Any
from typing_extensions import Literal

# 支持的像素格式
JPEGFormat = Literal[
    "RGB565_BE",    # RGB565 大端序
    "RGB565_LE",    # RGB565 小端序
    "CbYCrY",       # YUV 4:2:2
    "RGB888",       # RGB 24位
    "GRAY",         # 灰度
    "RGBA",         # RGBA 32位
    "YCbYCr",       # YUV 4:2:2 交错
    "YCbY2YCrY2"    # YUV 4:2:2 交错扩展
]

# 支持的旋转角度
JPEGRotation = Literal[0, 90, 180, 270]

# 支持的 JPEG 标准
JPEGStandard = Literal["JPEG", "MJPEG"]

class Decoder:
    """
    JPEG 解码器类
    
    用于解码 JPEG 图像数据, 支持多种输出格式, 旋转, 缩放和裁剪功能
    """
    
    def __init__(
        self,
        *,
        rotation: JPEGRotation = 0,
        format: Optional[JPEGFormat] = None,
        block: bool = False,
        scale_width: int = 0,
        scale_height: int = 0,
        clipper_width: int = 0,
        clipper_height: int = 0,
        return_bytes: bool = False
    ) -> None:
        """
        初始化 JPEG 解码器
        
        参数:
            rotation (JPEGRotation): 旋转角度 (0, 90, 180, 270)
            format (JPEGFormat): 输出像素格式
            block (bool): 是否启用分块解码
            scale_width (int): 缩放宽度
            scale_height (int): 缩放高度
            clipper_width (int): 裁剪宽度
            clipper_height (int): 裁剪高度
            return_bytes (bool): 是否返回 bytes 而不是 memoryview
        """
        ...
    
    def get_img_info(self, jpeg_data: Union[bytes, bytearray, memoryview]) -> List[int]:
        """
        获取 JPEG 图像信息
        
        参数:
            jpeg_data (Union[bytes, bytearray, memoryview]): JPEG 图像数据
            
        返回:
            (List[int]): 包含图像信息的列表 [width, height, block_count?, block_height?]
            如果启用分块解码, 还会返回块数量和每块高度
        """
        ...
    
    def decode(self, jpeg_data: Union[bytes, bytearray, memoryview]) -> Optional[Union[bytes, memoryview]]:
        """
        解码 JPEG 图像数据
        
        注意: 当使用分块解码模式时, 需要循环调用此方法直到返回 None
        
        参数:
            jpeg_data (Union[bytes, bytearray, memoryview]): JPEG 图像数据
            
        返回:
            (Union[bytes, memoryview]): 解码后的图像数据 (bytes 或 memoryview), 如果所有块都解码完则返回 None
        """
        ...
    
    def __enter__(self) -> "Decoder":
        """上下文管理器入口"""
        ...
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """上下文管理器出口, 自动释放资源"""
        ...
    
    def __del__(self) -> None:
        """析构函数, 释放资源"""
        ...


class Encoder:
    """
    JPEG 编码器类
    
    用于将图像数据编码为 JPEG 格式, 支持多种输入格式和质量控制
    """
    
    def __init__(
        self,
        width: int,
        height: int,
        format: JPEGFormat,
        *,
        quality: int = 90,
        rotation: JPEGRotation = 0
    ) -> None:
        """
        初始化 JPEG 编码器
        
        参数:
            width (int): 图像宽度
            height (int): 图像高度
            format (JPEGFormat): 输入像素格式
            quality (int): JPEG 质量 (1-100)
            rotation (JPEGRotation): 旋转角度
        """
        ...
    
    def encode(self, img_data: Union[bytes, bytearray, memoryview]) -> bytes:
        """
        编码图像数据为 JPEG
        
        参数:
            img_data (Union[bytes, bytearray, memoryview]): 输入图像数据
            
        返回:
            (bytes): 编码后的 JPEG 数据
        """
        ...
    
    def __enter__(self) -> "Encoder":
        """上下文管理器入口"""
        ...
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """上下文管理器出口, 自动释放资源"""
        ...
    
    def __del__(self) -> None:
        """析构函数, 释放资源"""
        ...


# 模块级函数和常量
def decode_jpeg(
    jpeg_data: Union[bytes, bytearray, memoryview],
    format: Optional[JPEGFormat] = None,
    rotation: JPEGRotation = 0
) -> Union[bytes, memoryview]:
    """
    快速解码 JPEG 数据的便捷函数
    
    参数:
        jpeg_data (Union[bytes, bytearray, memoryview]): JPEG 图像数据
        format (JPEGFormat): 输出格式
        rotation (JPEGRotation): 旋转角度
        
    返回:
        (Union[bytes, memoryview]): 解码后的图像数据
    """
    ...


def encode_jpeg(
    img_data: Union[bytes, bytearray, memoryview],
    width: int,
    height: int,
    format: JPEGFormat,
    quality: int = 90
) -> bytes:
    """
    快速编码图像数据为 JPEG 的便捷函数
    
    参数:
        img_data (Union[bytes, bytearray, memoryview]): 输入图像数据
        width (int): 图像宽度
        height (int): 图像高度
        format (JPEGFormat): 输入格式
        quality (int): JPEG 质量
        
    返回:
        (bytes): 编码后的 JPEG 数据
    """
    ...


# 错误类型
class JPEGError(Exception):
    """JPEG 编解码错误基类"""
    ...


class JPEGMemoryError(JPEGError):
    """内存不足错误"""
    ...


class JPEGValueError(JPEGError):
    """参数错误"""
    ...


class JPEGRuntimeError(JPEGError):
    """运行时错误"""
    ...


# 模块导出
__all__ = [
    "Decoder",
    "Encoder", 
    "decode_jpeg",
    "encode_jpeg",
    "JPEGError",
    "JPEGMemoryError",
    "JPEGValueError", 
    "JPEGRuntimeError",
    "JPEGFormat",
    "JPEGRotation"
]