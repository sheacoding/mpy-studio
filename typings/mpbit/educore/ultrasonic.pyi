from typing import Optional, Tuple


class ultrasonic:
    """
    超声波模块控制类,支持 I2C 和 GPIO 两种接口方式.

    根据传入参数自动识别使用哪种方式初始化传感器.
    """

    def __init__(
        self,
        *,
        sda: Optional[int] = None,
        scl: Optional[int] = None,
        trig: Optional[int] = None,
        echo: Optional[int] = None
    ) -> None:
        """
        初始化超声波模块.

        参数:
            sda (Optional[int]): I2C 数据线引脚编号(可选).
            scl (Optional[int]): I2C 时钟线引脚编号(可选).
            trig (Optional[int]): 触发信号引脚编号(可选).
            echo (Optional[int]): 回响信号引脚编号(可选).

        支持以下两种模式:
            - I2C 模式: 提供 sda 和 scl 引脚.
            - GPIO 模式: 提供 trig 和 echo 引脚.
        """
        ...

    def distance(self) -> int:
        """
        获取当前测距结果.

        返回:
            (int): 测距结果,单位为厘米(cm),范围为 0~200 cm.
        """
        ...