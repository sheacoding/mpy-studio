from mpbit import i2c_has_addr, i2c, Magnetic


class compass(object):
    """
    指南针类,用于获取磁力计方向和校准.
    """
    def __init__(self):
        """
        初始化指南针类,检查 I2C 地址是否可用.
        如果不可用,则打印错误信息并设置 _magnetic 为 None.
        """
        ...

    def adjust(self):
        """
        校准磁力计.
        如果 _magnetic 为 None,则直接返回.
        """
        ...

    def direction(self) -> float:
        """
        获取磁力计的方向.
        如果 _magnetic 为 None,则返回 None.

        返回:
            (float): 方向角度.
        """
        ...