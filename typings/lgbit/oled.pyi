from micropython import const
from machine import I2C, Pin
from typing import Optional, Union, Tuple, Any
from mpbit.mpin import MPin, PinMode  # 假设已有类型提示
from mpbit import get_i2c_bus, i2c_has_addr
from ssd1106 import SSD1106_I2C
from ssd1306 import SSD1306_I2C
import framebuf


class TextMode:
    """文本显示模式."""
    NORMAL = 1  # 正常显示.
    REV = 2     # 反色显示.
    TRANS = 3   # 透明显示.
    XOR = 4     # 异或显示.


class Font:
    """
    内置字体类,提供字体信息和字形数据.
    """
    def __init__(self) -> None:
        """
        初始化内置字体.
        
        字体信息包括:高度、宽度、基线、字符范围等.
        """
        ...

    def get_data(self, c: str) -> Optional[bytearray]:
        """
        获取指定字符的字形数据.

        参数:
            c (str): 要获取字形的字符.
            
        返回:
            (Optional[bytearray]): 字符对应的位图数据.
        """
        ...


class FrameBufUtil:
    """
    FrameBuffer 辅助工具类,提供各种图形绘制方法.
    """
    @staticmethod
    def circle(fb, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制圆轮廓.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x0 (int): 圆心 X 坐标.
            y0 (int): 圆心 Y 坐标.
            radius (int): 半径.
            c (int): 颜色(0 或 1).
        """
        ...

    @staticmethod
    def fill_circle(fb, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制填充圆.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x0 (int): 圆心 X 坐标.
            y0 (int): 圆心 Y 坐标.
            radius (int): 半径.
            c (int): 颜色(0 或 1).
        """
        ...

    @staticmethod
    def quarter_circle(fb, x0: int, y0: int, radius: int, cornername: int, c: int) -> None:
        """
        绘制四分之一圆弧.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x0 (int): 圆心 X 坐标.
            y0 (int): 圆心 Y 坐标.
            radius (int): 半径.
            cornername (int): 圆角标识(支持 0x1~0x8).
            c (int): 颜色(0 或 1).
        """
        ...

    @staticmethod
    def round_rect(fb, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制圆角矩形边框.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x (int): 左上角 X 坐标.
            y (int): 左上角 Y 坐标.
            w (int): 宽度.
            h (int): 高度.
            r (int): 圆角半径.
            color (int): 颜色(0 或 1),默认为 1.
        """
        ...

    @staticmethod
    def fill_round_rect(fb, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制填充圆角矩形.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x (int): 左上角 X 坐标.
            y (int): 左上角 Y 坐标.
            w (int): 宽度.
            h (int): 高度.
            r (int): 圆角半径.
            color (int): 颜色(0 或 1),默认为 1.
        """
        ...

    @staticmethod
    def triangle(fb, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制三角形边框.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x0 (int): 第一点 X 坐标.
            y0 (int): 第一点 Y 坐标.
            x1 (int): 第二点 X 坐标.
            y1 (int): 第二点 Y 坐标.
            x2 (int): 第三点 X 坐标.
            y2 (int): 第三点 Y 坐标.
            c (int): 颜色(0 或 1).
        """
        ...

    @staticmethod
    def fill_triangle(fb, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制填充三角形.

        参数:
            x0 (int): 第一点 X 坐标.
            y0 (int): 第一点 Y 坐标.
            x1 (int): 第二点 X 坐标.
            y1 (int): 第二点 Y 坐标.
            x2 (int): 第三点 X 坐标.
            y2 (int): 第三点 Y 坐标.
            c (int): 颜色(0 或 1).
        """
        ...

    @staticmethod
    def bitmap(fb, path: Union[str, bytes, bytearray], x: int, y: int, invert: int = 0) -> None:
        """
        在 OLED 上绘制图片.

        参数:
            fb: framebuf.FrameBuffer 实例.
            path (Union[str, bytes, bytearray]): 图片路径或直接传入图像数据.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            invert (int): 是否反色显示,默认不反色.
        """
        ...

    @staticmethod
    def draw_text(fb, sw: int, sh: int, s: str, x: int, y: int, mode: int = TextMode.NORMAL, wrap: bool = False) -> Tuple[int, Tuple[int, int]]:
        """
        在 OLED 上绘制文本.

        参数:
            fb: framebuf.FrameBuffer 实例.
            sw (int): 屏幕宽度.
            sh (int): 屏幕高度.
            s (str): 要绘制的字符串.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            mode (TextMode): 显示模式(NORMAL/REV/TRANS/XOR).
            wrap (bool): 是否自动换行.

        返回:
            (Tuple[int, Tuple[int, int]]): 文本总宽度和最后一个字符坐标位置.
        """
        ...

    @staticmethod
    def draw_font(
        fb, sw: int, sh: int, font: Any, s: str, x: int, y: int, invert: bool = False, wrap: bool = False
    ) -> Tuple[int, Tuple[int, int]]:
        """
        使用自定义字体在 OLED 上绘制文本.

        参数:
            fb: framebuf.FrameBuffer 实例.
            sw (int): 屏幕宽度.
            sh (int): 屏幕高度.
            font: 自定义字体对象.
            s (str): 要绘制的字符串.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            invert (bool): 是否反色显示.
            wrap (bool): 是否自动换行.

        返回:
            (Tuple[int, Tuple[int, int]]): 文本总宽度和最后一个字符坐标位置.
        """
        ...

    @staticmethod
    def progress_bar(fb, x: int, y: int, width: int, height: int, progress: int) -> None:
        """
        绘制进度条.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            width (int): 进度条宽度.
            height (int): 进度条高度.
            progress (int): 当前进度百分比(0 ~ 100).
        """
        ...

    @staticmethod
    def strip_bar(fb, x: int, y: int, width: int, height: int, progress: int, dir: int = 1, frame: int = 1) -> None:
        """
        绘制柱状条.

        参数:
            fb: framebuf.FrameBuffer 实例.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            width (int): 柱状条宽度.
            height (int): 柱状条高度.
            progress (int): 当前进度百分比(0 ~ 100).
            dir (int): 方向(1=水平,0=垂直).
            frame (int): 是否绘制外框.
        """
        ...

    @staticmethod
    def qr_code(fb, str: str, x: int, y: int, scale: int = 2) -> None:
        """
        绘制二维码.

        参数:
            fb: framebuf.FrameBuffer 实例.
            str (str): 要编码的内容.
            x (int): 起始 X 坐标.
            y (int): 起始 Y 坐标.
            scale (int): 缩放倍数.
        """
        ...


class OLED1106(SSD1106_I2C):
    def __init__(
        self,
        width: int = 128,
        height: int = 64,
        scl: int = 19,
        sda: int = 20,
        i2c: Optional[I2C] = None,
        addr: int = 0x3C,
        external_vcc: bool = False,
    ) -> None:
        """
        初始化 0.96 寸 OLED 屏幕（SSD1106 驱动)

        参数:
            width int: 屏幕宽度,默认 128
            height int: 屏幕高度,默认 64
            scl int: SCL 引脚编号
            sda int: SDA 引脚编号
            i2c (I2C): 外部 I2C 总线对象（可选)
            addr int: I2C 设备地址,默认 0x3C
            external_vcc (bool): 是否使用外部 VCC,默认否
        """
        ...

    def circle(self, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制圆轮廓

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            c int: 颜色（0 或 1)
        """
        ...

    def fill_circle(self, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制填充圆

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            c int: 颜色（0 或 1)
        """
        ...

    def quarter_circle(self, x0: int, y0: int, radius: int, cornername: int, c: int) -> None:
        """
        绘制四分之一圆弧

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            cornername int: 圆角标识（0x1~0x8)
            c int: 颜色（0 或 1)
        """
        ...

    def round_rect(self, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制圆角矩形边框

        参数:
            x int: 左上角 X 坐标
            y int: 左上角 Y 坐标
            w int: 宽度
            h int: 高度
            r int: 圆角半径
            color int: 颜色（0 或 1),默认为 1
        """
        ...

    def fill_round_rect(self, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制填充圆角矩形

        参数:
            x int: 左上角 X 坐标
            y int: 左上角 Y 坐标
            w int: 宽度
            h int: 高度
            r int: 圆角半径
            color int: 颜色（0 或 1),默认为 1
        """
        ...

    def triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制三角形边框

        参数:
            x0 int: 第一点 X 坐标
            y0 int: 第一点 Y 坐标
            x1 int: 第二点 X 坐标
            y1 int: 第二点 Y 坐标
            x2 int: 第三点 X 坐标
            y2 int: 第三点 Y 坐标
            c int: 颜色（0 或 1)
        """
        ...

    def fill_triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制填充三角形

        参数:
            x0 int: 第一点 X 坐标
            y0 int: 第一点 Y 坐标
            x1 int: 第二点 X 坐标
            y1 int: 第二点 Y 坐标
            x2 int: 第三点 X 坐标
            y2 int: 第三点 Y 坐标
            c int: 颜色（0 或 1)
        """
        ...

    def draw_text(self, s: str, x: int, y: int, mode: int = TextMode.NORMAL, wrap: bool = False) -> Tuple[int, Tuple[int, int]]:
        """
        在屏幕上绘制文本

        参数:
            s (str): 要绘制的字符串
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            mode (TextMode): 显示模式（NORMAL/REV/TRANS/XOR)
            wrap (bool): 是否自动换行

        返回:
            Tuple[int, Tuple[int, int]]: 文本总宽度和最后一个字符坐标位置
        """
        ...

    def draw_font(self, font: Any, s: str, x: int, y: int, invert: bool = False, wrap: bool = False) -> Tuple[int, Tuple[int, int]]:
        """
        使用自定义字体绘制文本

        参数:
            font: 字体对象
            s (str): 要绘制的字符串
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            invert (bool): 是否反色显示
            wrap (bool): 是否自动换行

        返回:
            Tuple[int, Tuple[int, int]]: 文本总宽度和最后一个字符坐标位置
        """
        ...

    def bitmap(self, path: Union[str, bytes, bytearray], x: int, y: int, invert: int = 0) -> None:
        """
        显示图片

        参数:
            path (str or bytes or bytearray): 图片路径或图像数据
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            invert int: 是否反色显示
        """
        ...

    def progress_bar(self, x: int, y: int, width: int, height: int, progress: int) -> None:
        """
        绘制进度条

        参数:
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            width int: 进度条宽度
            height int: 进度条高度
            progress int: 当前进度百分比（0 ~ 100)
        """
        ...

    def strip_bar(self, x: int, y: int, width: int, height: int, progress: int, dir: int = 1, frame: int = 1) -> None:
        """
        绘制柱状条

        参数:
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            width int: 柱状条宽度
            height int: 柱状条高度
            progress int: 当前进度百分比（0 ~ 100)
            dir int: 方向（1=水平,0=垂直)
            frame int: 是否绘制外框
        """
        ...

    def qr_code(self, str: str, x: int, y: int, scale: int = 2) -> None:
        """
        绘制二维码

        参数:
            str (str): 要编码的内容
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            scale int: 缩放倍数
        """
        ...


class OLED1306(SSD1306_I2C):
    def __init__(
        self, width: int = 128, height: int = 32, scl: int = 19, sda: int = 20, addr: int = 0x3C, external_vcc: bool = False
    ) -> None:
        """
        初始化 0.91 寸 OLED 屏幕（SSD1306 驱动)

        参数:
            width int: 屏幕宽度,默认 128
            height int: 屏幕高度,默认 32
            scl int: SCL 引脚编号
            sda int: SDA 引脚编号
            addr int: I2C 地址,默认 0x3C
            external_vcc (bool): 是否使用外部 VCC
        """
        ...

    def circle(self, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制圆轮廓

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            c int: 颜色（0 或 1)
        """
        ...

    def fill_circle(self, x0: int, y0: int, radius: int, c: int) -> None:
        """
        绘制填充圆

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            c int: 颜色（0 或 1)
        """
        ...

    def quarter_circle(self, x0: int, y0: int, radius: int, cornername: int, c: int) -> None:
        """
        绘制四分之一圆弧

        参数:
            x0 int: 圆心 X 坐标
            y0 int: 圆心 Y 坐标
            radius int: 半径
            cornername int: 圆角标识（0x1~0x8)
            c int: 颜色（0 或 1)
        """
        ...

    def round_rect(self, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制圆角矩形边框

        参数:
            x int: 左上角 X 坐标
            y int: 左上角 Y 坐标
            w int: 宽度
            h int: 高度
            r int: 圆角半径
            color int: 颜色（0 或 1),默认为 1
        """
        ...

    def fill_round_rect(self, x: int, y: int, w: int, h: int, r: int, color: int = 1) -> None:
        """
        绘制填充圆角矩形

        参数:
            x int: 左上角 X 坐标
            y int: 左上角 Y 坐标
            w int: 宽度
            h int: 高度
            r int: 圆角半径
            color int: 颜色（0 或 1),默认为 1
        """
        ...

    def triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制三角形边框

        参数:
            x0 int: 第一点 X 坐标
            y0 int: 第一点 Y 坐标
            x1 int: 第二点 X 坐标
            y1 int: 第二点 Y 坐标
            x2 int: 第三点 X 坐标
            y2 int: 第三点 Y 坐标
            c int: 颜色（0 或 1)
        """
        ...

    def fill_triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        绘制填充三角形

        参数:
            x0 int: 第一点 X 坐标
            y0 int: 第一点 Y 坐标
            x1 int: 第二点 X 坐标
            y1 int: 第二点 Y 坐标
            x2 int: 第三点 X 坐标
            y2 int: 第三点 Y 坐标
            c int: 颜色（0 或 1)
        """
        ...

    def draw_text(self, s: str, x: int, y: int, mode: int = TextMode.NORMAL, wrap: bool = False) -> Tuple[int, Tuple[int, int]]:
        """
        在屏幕上绘制文本

        参数:
            s (str): 要绘制的字符串
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            mode (TextMode): 显示模式（NORMAL/REV/TRANS/XOR)
            wrap (bool): 是否自动换行

        返回:
            Tuple[int, Tuple[int, int]]: 文本总宽度和最后一个字符坐标位置
        """
        ...

    def draw_font(self, font: Any, s: str, x: int, y: int, invert: bool = False, wrap: bool = False) -> Tuple[int, Tuple[int, int]]:
        """
        使用自定义字体绘制文本

        参数:
            font: 字体对象
            s (str): 要绘制的字符串
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            invert (bool): 是否反色显示
            wrap (bool): 是否自动换行

        返回:
            Tuple[int, Tuple[int, int]]: 文本总宽度和最后一个字符坐标位置
        """
        ...

    def bitmap(self, path: Union[str, bytes, bytearray], x: int, y: int, invert: int = 0) -> None:
        """
        显示图片

        参数:
            path (str or bytes or bytearray): 图片路径或图像数据
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            invert int: 是否反色显示
        """
        ...

    def progress_bar(self, x: int, y: int, width: int, height: int, progress: int) -> None:
        """
        绘制进度条

        参数:
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            width int: 进度条宽度
            height int: 进度条高度
            progress int: 当前进度百分比（0 ~ 100)
        """
        ...

    def strip_bar(self, x: int, y: int, width: int, height: int, progress: int, dir: int = 1, frame: int = 1) -> None:
        """
        绘制柱状条

        参数:
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            width int: 柱状条宽度
            height int: 柱状条高度
            progress int: 当前进度百分比（0 ~ 100)
            dir int: 方向（1=水平,0=垂直)
            frame int: 是否绘制外框
        """
        ...

    def qr_code(self, str: str, x: int, y: int, scale: int = 2) -> None:
        """
        绘制二维码

        参数:
            str (str): 要编码的内容
            x int: 起始 X 坐标
            y int: 起始 Y 坐标
            scale int: 缩放倍数
        """
        ...