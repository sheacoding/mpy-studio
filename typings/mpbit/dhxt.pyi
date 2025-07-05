from machine import Pin

class DHTBase:
    """
    DHT 系列传感器的基类.
    提供基础的初始化和测量方法.
    """

    def __init__(self, pin: Pin) -> None:
        """
        初始化传感器对象.

        参数:
          pin (Pin): 连接 DHT 传感器的引脚对象.
        """
        ...

    def measure(self) -> None:
        """
        从传感器中读取原始数据并进行校验.
        如果校验失败则重试一次,并打印错误信息.
        """
        ...

class DHT11(DHTBase):
    """
    DHT11 温湿度传感器驱动.
    继承自 DHTBase,提供具体的湿度和温度读取方法.
    """

    def humidity(self) -> int:
        """
        获取当前湿度值(单位:%RH).

        返回:
            (int): 湿度值.
        """
        ...

    def temperature(self) -> int:
        """
        获取当前温度值(单位:摄氏度).

        返回:
            (int): 温度值.
        """
        ...

class DHT22(DHTBase):
    """
    DHT22 (AM2302) 温湿度传感器驱动.
    继承自 DHTBase,支持更高精度的温湿度读取.
    """

    def humidity(self) -> float:
        """
        获取当前湿度值(单位:%RH).

        返回:
            (float): 湿度值(浮点数,精度为0.1%).
        """
        ...

    def temperature(self) -> float:
        """
        获取当前温度值(单位:摄氏度,支持负值).

        返回:
            (float): 温度值(浮点数,精度为0.1℃).
        """
        ...
