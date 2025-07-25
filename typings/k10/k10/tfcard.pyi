import typing

class TFCard:
    """
    TF卡单例类
    """
    _instance: typing.ClassVar[typing.Optional['TFCard']]
    is_available: bool
    mount_point: str

    def __init__(self, auto_mount: bool = True, mount_point: str = "/sd") -> None:
        """
        初始化 TFCard 对象
        参数:
            auto_mount (bool): 是否自动挂载
            mount_point (str): 挂载点路径
        返回:
            None: 无返回值
        """
        ...
    
    def deinit(self) -> None:
        """
        释放 SD 卡资源
        参数:
            无
        返回:
            None: 无返回值
        """
        ...

    def mount(self) -> bool:
        """
        挂载 SD 卡
        参数:
            无
        返回:
            bool: 挂载是否成功
        """
        ...

    def unmount(self) -> None:
        """
        卸载 SD 卡
        参数:
            无
        返回:
            None: 无返回值
        """
        ...