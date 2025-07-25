from typing import Optional
from oled import OLED1106

class OLED(OLED1106):
    """
    OLED 显示模块类,用于控制 OLED 屏幕。
    """

    def __init__(self, scl: int = 19, sda: int = 20, i2c: Optional[object] = None) -> None:
        """
        初始化 OLED 显示模块.

        参数:
            scl (int): I2C 时钟引脚,默认为 19.
            sda (int): I2C 数据引脚,默认为 20.
            i2c (Optional[object]): 自定义 I2C 实例,若未提供则使用默认配置.
        """
        ...

    def print(self, text: str) -> None:
        """
        在 OLED 屏幕上显示文本或表情.

        参数:
            text (str): 要显示的文本或表情标识符(如 "HAPPY" 或 "SAD").
        """
        ...

    def clear(self) -> None:
        """
        清空 OLED 屏幕.
        """
        ...