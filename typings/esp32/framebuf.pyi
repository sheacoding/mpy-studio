# framebuf.pyi

from __future__ import annotations
from typing import Any, Optional, overload, Final
from _typeshed import Incomplete
from _mpy_shed import AnyReadableBuf, AnyWritableBuf
from typing_extensions import Awaitable, TypeAlias, TypeVar

# 像素格式常量
MONO_HMSB: Final[int] = 4       # 单色水平MSB
MONO_HLSB: Final[int] = 3       # 单色水平LSB
RGB565: Final[int] = 1          # RGB565 格式
MONO_VLSB: Final[int] = 0       # 单色垂直LSB（常用)
MVLSB: Final[int] = 0           # 同 MONO_VLSB
GS2_HMSB: Final[int] = 5        # 2位灰度水平MSB
GS8: Final[int] = 6             # 8位灰度
GS4_HMSB: Final[int] = 2        # 4位灰度水平MSB

def FrameBuffer1(*args, **kwargs) -> Incomplete: ...

class FrameBuffer:
    """
    FrameBuffer 类提供了一个像素缓冲区,可用于绘制像素、线条、矩形、文本甚至其他 FrameBuffer 图像.
    它通常用于生成发送到显示屏的内容.

    示例::
    
        import framebuf

        # FrameBuffer 需要每个 RGB565 像素占用 2 字节
        fbuf = framebuf.FrameBuffer(bytearray(100 * 10 * 2), 100, 10, framebuf.RGB565)

        fbuf.fill(0)
        fbuf.text('MicroPython!', 0, 0, 0xffff)
        fbuf.hline(0, 9, 96, 0xffff)
    """

    def poly(self, x, y, coords, c, f: Optional[Any] = None) -> Incomplete:
        """
        给定一组坐标,在指定位置绘制任意（凸或凹)闭合多边形.
        
        参数:
            x: int 多边形的x坐标偏移
            y: int 多边形的y坐标偏移
            coords: (array) 坐标数组,格式为 array('h', [x0, y0, x1, y1, ... xn, yn])
            c: int 多边形的颜色值
            f: (bool) 可选,如果为True则填充多边形,否则只绘制轮廓
        """
        ...

    def vline(self, x: int, y: int, h: int, c: int, /) -> None:
        """
        绘制垂直线.
        
        参数:
            x: int 起始x坐标
            y: int 起始y坐标
            h: int 线的高度(像素)
            c: int 线的颜色值
        """
        ...

    @overload
    def pixel(self, x: int, y: int, /) -> int:
        """
        获取或设置像素颜色.
        
        参数:
            x: int 像素的x坐标
            y: int 像素的y坐标
            
        返回:
            int: 指定像素的颜色值
        """

    @overload
    def pixel(self, x: int, y: int, c: int, /) -> None:
        """
        获取或设置像素颜色.
        
        参数:
            x: int 像素的x坐标
            y: int 像素的y坐标
            c: int 要设置的颜色值
        """

    def text(self, s: str, x: int, y: int, c: int = 1, /) -> None:
        """
        在帧缓冲区上绘制文本.
        
        参数:
            s: str 要显示的文本字符串
            x: int 文本左上角的x坐标
            y: int 文本左上角的y坐标
            c: int 文本颜色,默认为1
            
        注意: 所有字符尺寸为8x8像素,目前无法更改字体.
        """
        ...

    def rect(self, x: int, y: int, w: int, h: int, c: int, f = False, /) -> None:
        """
        绘制矩形.
        
        参数:
            x: int 矩形左上角的x坐标
            y: int 矩形左上角的y坐标
            w: int 矩形宽度(像素)
            h: int 矩形高度(像素)
            c: int 矩形颜色
            f: (bool) 可选,如果为True则填充矩形,否则只绘制轮廓
        """
        ...

    def scroll(self, xstep: int, ystep: int, /) -> None:
        """
        滚动帧缓冲区内容.
        
        参数:
            xstep: int 水平滚动的像素数(正值向右,负值向左)
            ystep: int 垂直滚动的像素数(正值向下,负值向上)
            
        注意: 这可能会在帧缓冲区中留下之前颜色的痕迹.
        """
        ...

    def ellipse(self, x: int, y: int, xr: int, yr: int, c: int, f= False, m: Optional[int] = None) -> None:
        """
        绘制椭圆.
        
        参数:
            x: int 椭圆中心的x坐标
            y: int 椭圆中心的y坐标
            xr: int 椭圆x方向的半径
            yr: int 椭圆y方向的半径
            c: int 椭圆颜色
            f: bool 可选,如果为True则填充椭圆,否则只绘制轮廓
            m: int 可选,控制绘制哪些象限(位0=Q1,位1=Q2,位2=Q3,位3=Q4)
            
        注意: 象限按逆时针编号,Q1为右上角.
        """
        ...

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int, /) -> None:
        """
        绘制线段.
        
        参数:
            x1: int 起点x坐标
            y1: int 起点y坐标
            x2: int 终点x坐标
            y2: int 终点y坐标
            c: int 线的颜色
        """
        ...

    def blit(
        self,
        fbuf: FrameBuffer,
        x: int,
        y: int,
        key: int = -1,
        palette: Optional[bytes] = None,
        /,
    ) -> None:
        """
        将另一个帧缓冲区绘制到当前帧缓冲区上.
        
        参数:
            fbuf: FrameBuffer 源帧缓冲区
            x: int 目标位置的x坐标
            y: int 目标位置的y坐标
            key: int 可选,指定透明色值,默认为-1(无透明色)
            palette: bytes 可选,用于颜色映射的调色板
            
        注意: 如果指定了palette,它应该是一个与当前帧缓冲区格式相同的FrameBuffer实例,
        高度为1像素,宽度等于源帧缓冲区中的颜色数量.
        """
        ...

    def hline(self, x: int, y: int, w: int, c: int, /) -> None:
        """
        绘制水平线.
        
        参数:
            x: int 起始x坐标
            y: int 起始y坐标
            w: int 线的宽度(像素)
            c: int 线的颜色
        """
        ...

    def fill(self, c: int, /) -> None:
        """
        用指定颜色填充整个帧缓冲区.
        
        参数:
            c: int 填充颜色
        """
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int, /) -> None:
        """
        用指定颜色填充矩形区域.
        
        参数:
            x: int 矩形左上角的x坐标
            y: int 矩形左上角的y坐标
            w: int 矩形宽度(像素)
            h: int 矩形高度(像素)
            c: int 填充颜色
        """
        ...

    def __init__(
        self,
        buffer: AnyWritableBuf,
        width: int,
        height: int,
        format: int,
        stride: int = ...,
        /,
    ) -> None:
        """
        构造一个FrameBuffer对象.
        
        参数:
            buffer: (AnyWritableBuf) 支持缓冲协议的对象,用于存储像素数据
            width: int 帧缓冲区宽度(像素)
            height: int 帧缓冲区高度(像素)
            format: int 像素格式(如MONO_VLSB, RGB565等)
            stride: int 可选,每行像素之间的像素数,默认等于width
            
        注意: buffer必须足够大以容纳所有像素数据,格式决定了编码颜色所需的位数.
        """