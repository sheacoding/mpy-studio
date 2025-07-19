from typing import Tuple


class dht:
    """
    DHT 类用于读取 DHT11 温湿度传感器的数据.

    提供温度和湿度的读取接口.
    """

    def __init__(self, pin: int) -> None:
        """
        初始化 DHT 传感器对象.

        参数:
            pin (int): 使用的 GPIO 引脚编号.
        """
        ...

    def read(self) -> Tuple[float, float]:
        """
        读取当前温湿度数据.

        返回:
            (Tuple[float, float]): 包含温度(摄氏度)和湿度(百分比)的元组.
        """
        ...