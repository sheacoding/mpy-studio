from typing import Optional

class servo:
    """
    扩展 Servo 类,支持引脚单例模式管理.

    通过 remap 引脚作为唯一键,确保同一物理引脚只有一个舵机实例.
    """

    def __init__(self, pin: int) -> None:
        """
        初始化舵机对象,仅在首次创建时执行实际初始化.

        参数:
            pin (int): 使用的 PWM 引脚编号.
        """
        ...

    def angle(self, value: Optional[int] = None) -> Optional[int]:
        """
        获取或设置 180 度角度模式下的角度值.

        参数:
            value (Optional[int]): 要设置的角度值(0~180),若为 None 则表示获取当前角度.

        返回:
            (Optional[int]): 当前角度值(0~180).
        """
        ...