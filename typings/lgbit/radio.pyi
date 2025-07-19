import espnow
from ubinascii import hexlify, unhexlify
from typing import Optional, Callable, List, Tuple

class RadioESPNow:
    """
    RadioESPNow 类用于配置和管理 ESP-NOW 通信协议.
    支持发送和接收数据、设置频道、功率、加密等.
    """

    def __init__(self, channel: int = 1, txpower: int = 20) -> None:
        """
        初始化 RadioESPNow 实例.

        参数:
            channel (int): WiFi 信道,默认为 1.
            txpower (int): 发射功率,默认为 20 dBm.
        """
        ...

    def _cb_handle(self, espnow: espnow.ESPNow) -> None:
        """
        内部回调处理函数,用于处理接收到的数据.

        参数:
            espnow (espnow.ESPNow): ESPNow 对象.
        """
        ...

    def encrypt(self, peer: str, pmk: str, add_peer: bool = True) -> None:
        """
        设置预共享密钥并选择性地添加对等设备.

        参数:
            peer (str): 对等设备的 MAC 地址(十六进制字符串).
            pmk (str): 预共享密钥.
            add_peer (bool): 是否添加对等设备,默认为 True.
        """
        ...

    def on(self) -> None:
        """
        激活 ESP-NOW 接口.
        """
        ...

    def off(self) -> None:
        """
        去激活 ESP-NOW 接口.
        """
        ...

    def send(self, peer: str = 'ffffffffffff', msg: str = '') -> bool:
        """
        向指定对等设备发送消息.

        参数:
            peer (str): 对等设备的 MAC 地址(十六进制字符串),默认为广播地址.
            msg (str): 要发送的消息,默认为空字符串.

        返回:
            (bool): 发送成功与否的状态.
        """
        ...

    def recv(self) -> Tuple[Optional[str], Optional[str]]:
        """
        接收来自对等设备的消息.

        返回:
            (Tuple[Optional[str], Optional[str]]): (MAC地址, 消息内容),若无数据则返回 (None, None).
        """
        ...

    def set_channel(self, channel: int) -> None:
        """
        设置 WiFi 信道.

        参数:
            channel (int): 新的 WiFi 信道.
        """
        ...

    def set_txpower(self, txpower: int) -> None:
        """
        设置发射功率.

        参数:
            txpower (int): 新的发射功率值(dBm).
        """
        ...

    def set_recv_handler(self, callback: Callable[[str, str], None]) -> None:
        """
        设置接收消息时的回调函数.

        参数:
            callback (Callable[[str, str], None]): 当收到消息时调用的函数.
        """
        ...

    def add_certain_handler(self, certain: str, callback: Callable[[], None]) -> None:
        """
        为特定消息添加回调函数.

        参数:
            certain (str): 触发回调的特定消息.
            callback (Callable[[], None]): 回调函数.
        """
        ...

    def info(self) -> List[Tuple[str, int]]:
        """
        获取所有对等设备的信息.

        返回:
            (List[Tuple[str, int]]): 列表形式的对等设备信息,每个元素是 (MAC地址, 状态).
        """
        ...

    @property
    def mac(self) -> str:
        """
        获取本机 MAC 地址.
        """
        ...

    @property
    def channel(self) -> int:
        """
        获取当前 WiFi 信道.
        """
        ...