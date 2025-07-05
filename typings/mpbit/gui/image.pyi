from typing import Optional, Union, Tuple, List, Any
from framebuf import FrameBuffer

class Image:
    """图像处理类,支持加载和处理PBM和BMP格式的图像.
    """
    
    def __init__(self, invert: int = 0) -> None:
        """
        初始化图像对象.
        
        参数:
            invert (int): 是否反转图像像素值,0表示不反转,1表示反转.
        """
        ...

    
    def load(self, path: str) -> Optional[FrameBuffer]:
        """
        从文件加载图像.
        
        参数:
            path (str): 图像文件路径.
            
        返回:
            (Optional[FrameBuffer]): 包含加载的图像数据,加载失败返回None.
        """
        ...
    
    def load_bytes(self, bytes: Union[bytes, bytearray]) -> FrameBuffer:
        """
        从字节数组加载图像.
        
        参数:
            bytes (Union[bytes, bytearray]): 包含图像数据的字节数组.
            
        返回:
            (FrameBuffer): 包含加载的图像数据.
        """
        ...
    
    @property
    def width(self) -> int:
        """
        获取图像宽度.

        返回:
            (int): 图像宽度.
        """
        ...
    
    @property
    def height(self) -> int:
        """
        获取图像高度.

        返回:
            (int): 图像高度.
        """
        ... 