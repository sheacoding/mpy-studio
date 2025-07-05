class rfid:
    """
    RFID 类用于控制 RC522 射频识别模块.

    提供查找卡片和读取卡号等基础功能.
    """

    def __init__(self, scl: int = 0, sda: int = 1) -> None:
        """
        初始化 RFID 模块.

        参数:
            scl (int): I2C 时钟引脚编号,默认为 0.
            sda (int): I2C 数据引脚编号,默认为 1.
        """
        ...

    def find_card(self) -> bool:
        """
        查找是否检测到 RFID 卡片.

        返回:
            (bool): 如果检测到卡片返回 True,否则返回 False.
        """
        ...

    def serial_number(self) -> bytes:
        """
        读取当前卡片的序列号(ID).

        返回:
            (bytes): 卡片的 4 字节序列号.
        """
        ...