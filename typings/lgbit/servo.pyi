class Servo:
    """
    Servo 类用于控制舵机的角度或连续旋转速度.

    支持 180 度角度控制和 360 度连续旋转速度控制.
    """

    def __init__(self, pin: int) -> None:
        """
        初始化舵机对象.

        参数:
            pin (int): 使用的 PWM 引脚编号.
        """
        ...

    def get_180_angle(self) -> int:
        """
        获取当前设置的 180 度模式下的角度.

        返回:
            (int): 当前角度值,范围 [0, 180].
        """
        ...

    def set_180_angle(self, angle: int) -> None:
        """
        设置 180 度模式下的角度.

        参数:
            angle (int): 目标角度,范围 [0, 180].
        """
        ...

    def get_360_speed(self) -> int:
        """
        获取当前设置的 360 度模式下的速度.

        返回:
            (int): 当前速度值,范围 [-100, 100].
        """
        ...

    def set_360_speed(self, speed: int) -> None:
        """
        设置 360 度模式下的旋转速度.

        参数:
            speed (int): 速度值,范围 [-100, 100].
        """
        ...