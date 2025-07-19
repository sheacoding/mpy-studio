"""
DS18B20数字温度传感器类型提示.

DS18B20是一种常用的单总线数字温度传感器,精度高、功耗低.
"""

from machine import Pin
from typing import List, Optional

class ds18b20:
    """
    DS18B20数字温度传感器驱动类.
    
    该传感器使用单总线协议,可测量-55°C到+125°C范围内的温度.
    精度为±0.5°C(在-10°C到+85°C范围内).
    """
    
    def __init__(self, pin: int) -> None:
        """
        初始化DS18B20传感器.
        
        参数:
            pin (int): 传感器连接的引脚编号
        """
        self._pin: int = ...
        self.dat: Pin = ...
        self.ds = ...  # DS18X20 对象

    def read(self) -> float:
        """
        读取当前温度.
        
        返回:
            (float): 当前温度,单位为摄氏度
            
        注意: 
            - 如果总线上没有设备,将会引发索引错误
            - 读取过程需要至少750ms
        """
        ... 