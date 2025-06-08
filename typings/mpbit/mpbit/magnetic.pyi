from machine import I2C


class Magnetic:
    def __init__(self, i2c: I2C) -> None:
        """
        初始化磁力计传感器
        
        参数:
            i2c (I2C): 已初始化的 I2C 总线实例
        """
        ...

    def peeling(self) -> None:
        """
        设置当前磁场环境为“零点”，类似电子秤去皮功能。
        用于消除背景磁场干扰。
        """
        ...

    def clear_peeling(self) -> None:
        """
        清除已设置的去皮偏移值。
        """
        ...

    def get_x(self) -> float:
        """
        获取 X 轴磁场强度（单位：mG）
        
        返回:
            float: X 轴磁场值
        """
        ...

    def get_y(self) -> float:
        """
        获取 Y 轴磁场强度（单位：mG）
        
        返回:
            float: Y 轴磁场值
        """
        ...

    def get_z(self) -> float:
        """
        获取 Z 轴磁场强度（单位：mG）
        
        返回:
            float: Z 轴磁场值
        """
        ...

    def get_field_strength(self) -> float:
        """
        获取当前磁场总强度（三维向量模长）

        返回:
            float: 磁场强度（单位：mG）
        """
        ...

    def calibrate(self) -> None:
        """
        进行磁场校准，需要将设备旋转一周以上以获取最大最小值。

        校准后会更新内部偏移值，提升方向检测精度。
        """
        ...

    def get_heading(self) -> float:
        """
        获取当前方位角（0~360度），表示设备相对于北方的方向

        返回:
            float: 方位角（单位：度）
        """
        ...