from machine import WLAN
from typing import Optional


class WiFi:
    def __init__(self) -> None:
        """
        初始化 WiFi 模块，支持 STA(客户端)和 AP(热点)模式。
        """
        ...

    def connect(self, ssid: str, passwd: str, timeout: int = 10) -> None:
        """
        连接到指定的 WiFi 网络
        
        参数:
            ssid (str): 要连接的无线网络名称
            passwd (str): 密码
            timeout (int): 连接超时时间（秒），默认 10 秒
            
        抛出:
            OSError: 如果 SSID 不存在或连接超时
        """
        ...

    def disconnect(self) -> None:
        """
        断开当前连接的 WiFi(STA 模式)
        """
        ...

    def enable_ap_wifi(self, essid: str, password: bytes = b"", channel: int = 10) -> None:
        """
        启用 AP(热点)模式
        
        参数:
            essid (str): 热点名称
            password (bytes): 热点密码（为空表示无密码）
            channel (int): 信道，默认为 10
        """
        ...

    def disable_ap_wifi(self) -> None:
        """
        禁用 AP(热点)模式
        """
        ...