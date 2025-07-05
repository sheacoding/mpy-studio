from typing import Optional, Union, Any, Tuple

import lvgl as lv
import machine
from k10.tca9555 import TCA9555

class Screen:
    """显示屏控制类"""

    canvas: lv.obj

    def __init__(self, tca9555: TCA9555 | None = None) -> None:
        """
        初始化显示屏对象, 但不开启电源
        
        参数:
            tca9555 (TCA9555 | None): TCA9555 IO扩展器对象, 默认为None
        """
        ...

    def init(self, dir: int = 2) -> None:
        """
        初始化屏幕, 设置方向, 并确保电源开启
        
        参数:
            dir (int): 屏幕方向, 0-3分别对应0度, 90度, 180度, 270度
        """
        ...

    def draw_img(
        self, x: int, y: int, w: int, h: int, img: Union[str, Any]
    ) -> Optional[lv.image]:
        """
        在屏幕上显示图像
        
        参数:
            x (int): 图像左上角的X坐标
            y (int): 图像左上角的Y坐标
            w (int): 图像宽度
            h (int): 图像高度
            img (Union[str, Any]): 图像数据, 可以是文件路径或图像对象

        返回:
            (Optional[lv.image]): 创建的图像对象, 加载失败则返回None
        """
        ...

    def draw_text(
        self, text: str = "hello", line: int = 0, color: int = 0xFFFFFF
    ) -> Optional[lv.label]:
        """
        在屏幕上显示文本
        
        参数:
            text (str): 要显示的文本
            line (int): 行号(从0开始)
            color (int): 文本颜色, 十六进制RGB值

        返回:
            (Optional[lv.label]): 创建的标签对象, 失败则返回None
        """
        ...

    def _init_canvas(self) -> None:
        """初始化画布, 设置黑色背景"""
        ...

    def _reset_canvas(self) -> None:
        """重置画布背景为黑色"""
        ...
