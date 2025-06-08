from mpbit import MPin
from typing import Optional

class light:
    """
    light 类用于读取光线传感器的模拟值。

    参数:
        pin (int, 可选): 指定连接光线传感器的引脚编号，默认为 None.

    方法:
        read: 根据传感器类型读取模拟值.
    """

    def __init__(self, pin: Optional[int] = None) -> None:
        """
        初始化 light 类实例.

        如果未指定 pin,则使用内置光线传感器;否则使用外接光线传感器.
        """
        ...

    def read(self) -> int:
        """
        读取光线传感器的模拟值.

        返回:
            int: 光线传感器的模拟数值.
        """
        ...