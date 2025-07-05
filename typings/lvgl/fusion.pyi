from typing import Callable, Tuple


class Fusion:

    def __init__(self, declination: float | None = None):
        """
        初始化传感器融合
        
        参数:
            declination (float | None): 磁偏角，默认None
        返回:
            (None): 无返回值
        """
        ...

    def calibrate(self, mag_xyz: Callable[[], Tuple[float, float, float]], stopfunc: Callable[[], bool], /):
        """
        校准传感器
        
        参数:
            mag_xyz (Callable[[], Tuple[float, float, float]]): 磁力计XYZ数据获取函数
            stopfunc (Callable[[], bool]): 停止校准函数
        返回:
            (None): 无返回值
        """
        ...

    def update(self,
        accel: Tuple[float, float, float],
        gyro: Tuple[float, float, float],
        mag: Tuple[float, float, float] | None = None
    ) -> Tuple[float, float, float]:
        """
        更新传感器数据
        
        参数:
            accel (Tuple[float, float, float]): 加速度计数据
            gyro (Tuple[float, float, float]): 陀螺仪数据
            mag (Tuple[float, float, float] | None): 磁力计数据，默认None
        返回:
            (Tuple[float, float, float]): 融合后的姿态数据
        """
        ...
