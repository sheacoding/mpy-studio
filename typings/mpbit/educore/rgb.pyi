from typing import List, Optional

class rgb:
    """
    RGB 类用于控制 RGB LED 灯带.
    """

    def __init__(self, pin: Optional[int] = None) -> None:
        """
        初始化一个 RGB 灯带对象.

        参数:
            pin (Optional[int]): 外接灯带连接的引脚编号.若为 None 表示使用板载灯带.
        """
        ...

    def write(self, index: List[int] = [0, 1, 2], r: int = 0, g: int = 0, b: int = 0) -> None:
        """
        设置指定灯珠的颜色并立即显示.

        参数:
            index (List[int]): 要设置的灯珠索引列表,默认为 [0, 1, 2].
            r (int): 红色通道值(0-255).
            g (int): 绿色通道值(0-255).
            b (int): 蓝色通道值(0-255).
        """
        ...

    def clear(self) -> None:
        """
        关闭所有灯珠,清空显示.
        """
        ...