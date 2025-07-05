from typing import Optional, Callable, Any


class MqttClient:
    """
    MQTT 客户端类,用于连接 MQTT 服务器并实现消息发布与订阅功能.
    """

    def __init__(self) -> None:
        """
        初始化 MQTT 客户端对象.
        """
        ...

    def connect(self, **kwargs: Any) -> None:
        """
        连接到指定的 MQTT Broker.

        参数:
            server (str): MQTT 服务器地址,默认为 "iot.mpython.cn".
            port (int): 端口号,默认为 1883.
            client_id (str): 客户端 ID,默认为空.
            user (str): 登录用户名,默认为空.
            psd (str): 登录密码,默认为空.
            password (str): 同 psd,兼容性参数.
        """
        ...

    def connected(self) -> bool:
        """
        获取当前 MQTT 连接状态.

        返回:
            (bool): 如果已连接到 MQTT Broker,返回 True;否则返回 False.
        """
        ...

    def publish(self, topic: str, content: str) -> None:
        """
        发布消息到指定主题.

        参数:
            topic (str): 主题名称.
            content (str): 要发布的消息内容.
        """
        ...

    def message(self, topic: str) -> Optional[str]:
        """
        获取指定主题的最新消息.

        参数:
            topic (str): 主题名称.

        返回:
            (str): 最新消息内容,如果没有消息则为 None.
        """
        ...

    def received(self, topic: str, callback: Callable[[], None]) -> None:
        """
        注册指定主题的消息回调函数.

        参数:
            topic (str): 主题名称.
            callback (Callable[[], None]): 收到消息时执行的回调函数.
        """
        ...

    def subscribe(self, topic: str, callback: Callable[[], None]) -> None:
        """
        订阅指定主题,并绑定回调函数.

        参数:
            topic (str): 主题名称.
            callback (Callable[[], None]): 收到消息时执行的回调函数.
        """
        ...