# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Tuple

import lvgl as lv

style: lv.style_t = ...


class Tpcal_point(object):

    def __init__(self, x, y, name):
        """
        初始化触摸校准点
        
        参数:
            x: X坐标
            y: Y坐标
            name: 点名称
        返回:
            (None): 无返回值
        """
        ...

    def __repr__(self):
        """
        字符串表示
        
        参数:
            无
        返回:
            (str): 字符串表示
        """
        ...


class Tpcal(object):

    def __init__(self, touch_count=500):
        """
        初始化触摸校准器
        
        参数:
            touch_count (int): 触摸计数，默认500
        返回:
            (None): 无返回值
        """
        ...

    def show_text(self, txt):
        """
        显示文本
        
        参数:
            txt: 要显示的文本
        返回:
            (None): 无返回值
        """
        ...

    def show_circle(self):
        """
        显示圆圈
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def calibrate_clicked(self, x, y):
        """
        校准点击事件
        
        参数:
            x: X坐标
            y: Y坐标
        返回:
            (None): 无返回值
        """
        ...

    def check(self):
        """
        检查校准状态
        
        参数:
            无
        返回:
            (bool): 校准状态
        """
        ...

    def calibrate(self, points) -> Tuple[(int, int, int, int)]:
        """
        执行校准
        
        参数:
            points: 校准点
        返回:
            (Tuple[(int, int, int, int)]): 校准结果
        """
        ...


# Run calibration
def run():
    """
    运行校准程序
    
    参数:
        无
    返回:
        (None): 无返回值
    """
    ...

