from typing import Callable, Optional

__version__: str = ...

class NEC_RX:
    """
    红外遥控接收类,用于解码 NEC 协议的红外信号.
    """

    def __init__(self, pin: int, callback: Optional[Callable[[int, int], None]] = None, timeout: int = 15000, timer_id: int = 1) -> None:
        """
        初始化红外接收器.

        参数:
            pin (int): 接收红外信号的 GPIO 引脚号.
            callback (Optional[Callable[[int, int], None]]): 接收到有效信号时调用的回调函数,参数为命令(cmd)和地址(addr).
            timeout (int): 超时时间(微秒),用于判断帧是否接收完成.
            timer_id (int): 使用的定时器 ID.
        """
        ...

    def decode(self) -> bool:
        """
        解码 NEC 红外协议的数据帧.

        返回:
            (bool): 解码是否成功.
        """
        ...