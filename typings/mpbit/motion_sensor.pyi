# motion_sensor.pyi
from typing import Callable, Optional

# 倾斜方向常量定义(用于 MotionTilt 类)
class TiltDir:
    NONE: int              # 无倾斜.
    FORWARD: int           # 向前倾斜(平放状态).
    BACK: int              # 向后倾斜(平放状态).
    RIGHT: int             # 向右倾斜(平放状态).
    LEFT: int              # 向左倾斜(平放状态).
    STAND_FORWARD: int     # 立起向前倾斜.
    STAND_BACK: int        # 立起向后倾斜.
    STAND_LEFT: int        # 立起向左倾斜.
    STAND_RIGHT: int       # 立起向右倾斜.


# 模拟 accelerometer 接口(实际来自 mpbit)
class accelerometer:
    """
    加速度传感器接口模拟类.
    """
    @staticmethod
    def get_x() -> float:
        """
        获取 X 轴加速度值.
        """
        ...

    @staticmethod
    def get_y() -> float:
        """
        获取 Y 轴加速度值.
        """
        ...

    @staticmethod
    def get_z() -> float:
        """
        获取 Z 轴加速度值.
        """
        ...


# 监控设备是否被摇晃或抛起的类
class MotionShakedOrThrown:
    """
    设备摇晃或抛起检测类.
    """
    def __init__(self) -> None:
        """
        初始化摇晃/抛起检测器.
        使用定时器定期检测加速度变化并触发回调.
        """
        ...

    def deinit(self) -> None:
        """
        停止检测,移除定时任务.
        在对象销毁时调用以释放资源.
        """
        ...

    def get_is_shaked(self) -> bool:
        """
        获取当前是否处于摇晃状态.
        
        返回:
            (bool): 是否正在摇晃.
        """
        ...

    def get_is_thrown(self) -> bool:
        """
        获取当前是否处于抛起状态.

        返回:
            (bool): 是否正在抛起.
        """
        ...

    # 回调函数
    on_shaked: Callable[[], None]   # 当设备被摇晃时调用.
    on_thrown: Callable[[], None]   # 当设备被抛起时调用.


# 监控设备倾斜状态的类
class MotionTilt:
    """
    设备倾斜状态监控类.
    """
    def __init__(self) -> None:
        """
        初始化倾斜检测器.
        支持识别设备在平放或立起状态下的多个方向倾斜.
        """
        ...

    def deinit(self) -> None:
        """
        停止检测,移除定时任务.
        在对象销毁时调用以释放资源.
        """
        ...

    # 平放状态下的回调
    on_tilt_forward: Callable[[], None]   # 设备向前倾斜时调用.
    on_tilt_back: Callable[[], None]      # 设备向后倾斜时调用.
    on_tilt_right: Callable[[], None]     # 设备向右倾斜时调用.
    on_tilt_left: Callable[[], None]      # 设备向左倾斜时调用.
    on_tilt_none: Callable[[], None]      # 没有明显倾斜时调用.

    # 立起状态下的回调
    on_stand_tilt_forward: Callable[[], None]  # 立起时向前倾斜.
    on_stand_tilt_back: Callable[[], None]     # 立起时向后倾斜.
    on_stand_tilt_left: Callable[[], None]     # 立起时向左倾斜.
    on_stand_tilt_right: Callable[[], None]    # 立起时向右倾斜.
    on_stand_tilt_none: Callable[[], None]     # 立起时无明显倾斜.

    @staticmethod
    def check_dir(dir: int) -> bool:
        """
        静态方法: 根据给定方向判断当前是否符合该倾斜状态.

        参数:
            dir (int): 方向常量(来自 TiltDir).

        返回:
            (bool): 是否符合该方向.
        """
        ...