"""
超声波测距模块HC-SR04的驱动类型提示.

HC-SR04是一种常用的超声波测距传感器,可测量2cm-400cm范围内的距离.
"""

from machine import Pin
from typing import Final

class HCSR04:
    """
    超声波测距模块HC-SR04驱动,测量范围2cm-400cm.
    
    此模块通过发送超声波脉冲并测量回波时间来计算距离.
    超时会抛出OSError('Out of range').
    """
    
    def __init__(self, trigger_pin: int, echo_pin: int, echo_timeout_us: int = 30000) -> None:
        """
        初始化HC-SR04超声波传感器.
        
        参数:
            trigger_pin (int): 触发引脚编号(输出).
            echo_pin (int): 回响引脚编号(输入,建议串1k电阻).
            echo_timeout_us (int): 超时时间(微秒),默认30000μs(30ms).
        """
        self.echo_timeout_us: int = echo_timeout_us
        self.trigger: Pin = Pin(trigger_pin, mode=Pin.OUT)
        self.echo: Pin = Pin(echo_pin, mode=Pin.IN)
        self.__limit: Final[int] = 400  # 最大测量距离cm
    
    def _send_pulse_and_wait(self) -> int:
        """
        发送触发脉冲并等待回响.
        
        返回:
            (int): 脉冲持续时间(微秒).
                -1: 测量过程中超时.
                -2: 等待初始电平变化时超时.
        """
        ...
    
    def distance_mm(self) -> int:
        """
        获取距离(毫米).
        
        返回:
            (int): 测量的距离(毫米),如果超出范围则返回最大距离限制值(4000mm).
        """
        ...
    
    def distance_cm(self) -> float:
        """
        获取距离(厘米).
        
        返回:
            (float): 测量的距离(厘米),如果超出范围则返回最大距离限制值(400cm).
        """
        ... 