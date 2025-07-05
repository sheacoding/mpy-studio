from typing import Optional, Tuple

class WiFi:
    """
    WiFi 类用于简化 ESP32 的 WiFi 连接与状态查询操作.
    
    继承自 mpbit.wifi.WiFi 类,封装了常用的连接和状态方法.
    """

    def __init__(self) -> None:
        """
        初始化 WiFi 模块.
        
        调用父类构造函数以初始化底层网络接口.
        """
        ...

    def connect(self, ssid: str, psd: str, timeout: int = 10000) -> None:
        """
        连接到指定的 WiFi 网络.

        参数:
            ssid (str): 要连接的 WiFi 名称.
            psd (str): WiFi 密码.
            timeout (int): 连接超时时间(单位:毫秒),默认为 10000 毫秒.
        """
        ...

    def status(self) -> bool:
        """
        获取当前 WiFi 连接状态.

        返回:
            (bool): 如果已连接到 WiFi,返回 True;否则返回 False.
        """
        ...

    def info(self) -> str:
        """
        获取当前 STA 接口的网络配置信息.

        返回:
            (str): 包含 IP 地址、子网掩码、网关和 DNS 的字符串表示.
        """
        ...