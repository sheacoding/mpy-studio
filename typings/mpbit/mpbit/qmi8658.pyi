from typing import Optional, Tuple, Callable, Any, Union
from machine import I2C, Pin
import ustruct
import math
from micropython import schedule
from esp32 import NVS
from mpbit.axis import Axis
from timer_manager import TimerManager
from mpbit import i2c_has_addr


class QMI8658:
    """QMI8658 6轴传感器实现"""

    IIC_ADDR: int = 107  # 0x6B

    def __init__(self, i2c: I2C) -> None:
        """
        初始化QMI8658传感器
        Args:
            i2c: I2C总线实例
        """
        ...

    def get_fw_version(self) -> bytes:
        """
        获取固件版本
        Returns:
            固件版本号（bytes）
        """
        ...

    class Accelerometer:
        """QMI8658加速度计实现"""

        RANGE_2G: int
        RANGE_4G: int
        RANGE_8G: int
        RANGE_16G: int

        RES_14_BIT: int
        RES_12_BIT: int
        RES_10_BIT: int

        def __init__(self, parent: "QMI8658") -> None:
            """
            初始化加速度计
            Args:
                parent: QMI8658实例
            """
            ...

        def set_range(self, range: int) -> None:
            """
            设置量程
            Args:
                range: 加速度计量程常量
            """
            ...

        def get_x(self) -> float:
            """获取X轴加速度值"""
            ...

        def get_y(self) -> float:
            """获取Y轴加速度值"""
            ...

        def get_z(self) -> float:
            """获取Z轴加速度值"""
            ...

        def set_offset(self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None) -> None:
            """
            设置偏移值
            Args:
                x: X轴偏移值
                y: Y轴偏移值
                z: Z轴偏移值
            """
            ...

        def get_roll(self) -> float:
            """获取横滚角"""
            ...

        def get_pitch(self) -> float:
            """获取俯仰角"""
            ...

        def get_tilt_angle(self, axis: Axis) -> float:
            """
            获取倾斜角度
            Args:
                axis: 轴向（Axis.X/Y/Z）
            Returns:
                float: 倾斜角度
            """
            ...

    class Gyroscope:
        """QMI8658陀螺仪实现"""

        RANGE_16_DPS: int
        RANGE_32_DPS: int
        RANGE_64_DPS: int
        RANGE_128_DPS: int
        RANGE_256_DPS: int
        RANGE_512_DPS: int
        RANGE_1024_DPS: int
        RANGE_2048_DPS: int

        def __init__(self, parent: "QMI8658") -> None:
            """
            初始化陀螺仪
            Args:
                parent: QMI8658实例
            """
            ...

        def set_range(self, range: int) -> None:
            """
            设置量程
            Args:
                range: 陀螺仪量程常量
            """
            ...

        def set_odr(self, odr: int) -> None:
            """
            设置输出数据率
            Args:
                odr: 输出数据率
            """
            ...

        def get_x(self) -> float:
            """获取X轴角速度值"""
            ...

        def get_y(self) -> float:
            """获取Y轴角速度值"""
            ...

        def get_z(self) -> float:
            """获取Z轴角速度值"""
            ...

        def set_offset(self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None) -> None:
            """
            设置偏移值
            Args:
                x: X轴偏移值
                y: Y轴偏移值
                z: Z轴偏移值
            """
            ...