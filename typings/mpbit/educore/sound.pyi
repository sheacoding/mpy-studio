from mpbit import MPin, PinMode, sound as _sound
from typing import Optional

class sound:
    """
    sound 类用于读取声音传感器的模拟值。
    
    说明：
        支持内置或外接声音传感器，通过 read 方法获取模拟值。
    """

    def __init__(self, pin: Optional[int] = None) -> None:
        """
        初始化 sound 类实例。

        参数:
            pin (Optional[int], optional): 指定连接声音传感器的引脚编号，默认为 None。
        """
        ...

    def read(self) -> int:
        """
        读取声音传感器的模拟值。

        返回:
            int: 声音传感器的模拟数值。
        """
        ...