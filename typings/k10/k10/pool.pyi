from k10.screen import Screen
from k10.speaker import Speaker

class Pool:
    """
    对象池类
    """

    def __init__(self) -> None:
        """
        初始化对象池
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def __str__(self) -> str:
        """
        返回对象池的字符串表示
        参数:
            无
        返回:
            (str): 对象池的字符串信息
        """
        ...

    def __repr__(self) -> str:
        """
        返回对象池的详细字符串表示
        参数:
            无
        返回:
            (str): 对象池的详细字符串信息
        """
        ...

    def __del__(self) -> None:
        """
        析构函数,自动释放资源
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def deinit(self) -> None:
        """
        释放对象池资源
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def get(self, key: str) -> Screen | Speaker | None:
        """
        获取对象
        参数:
            key (str): 对象的键名
        返回:
            (object): 获取到的对象,若不存在返回 None
        """
        ...

    def put(self, key: str, obj: object) -> None:
        """
        放入对象
        参数:
            key (str): 对象的键名
            obj (object): 要放入的对象
        返回:
            (None): 无返回值
        """
        ...
