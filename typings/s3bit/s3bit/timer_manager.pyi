from typing import Any, Callable, List, Optional, Tuple

class TimerManager:
    """
    定时任务管理器,用于管理和调度定时任务(如循环执行或延迟执行).
    """

    @classmethod
    def _init(cls) -> None:
        """
        初始化定时器.如果任务队列不为空,则启动硬件定时器.此方法通常在添加任务时自动调用.
        """
        ...

    @classmethod
    def loop(cls, period: int, cb:Callable[[],None]) -> None:
        """
        添加一个循环任务,在指定周期(毫秒)内重复执行回调函数.

        参数:
            period (int): 执行间隔时间(毫秒).
            cb (Callable[[], None]): 要执行的回调函数,可为 None.
        """
        ...

    @classmethod
    def delay(cls, period: int, cb: Callable[[], None]) -> None:
        """
        添加一个延迟任务,在指定时间(毫秒)后执行一次回调函数.

        参数:
            period (int): 延迟时间(毫秒).
            cb (Optional[Callable[[Any], None]]): 要执行的回调函数,可为 None.
        """
        ...

    @classmethod
    def remove(cls, cb: Callable[[], None]) -> None:
        """
        移除与指定回调函数匹配的任务.

        参数:
            cb (Optional[Callable[[Any], None]]): 要移除的回调函数,可为 None.
        """
        ...

    @classmethod
    def _check(cls, _: Any) -> None:
        """
        定时器回调函数,用于检查并执行到期的任务.

        参数:
            _ (Any): 定时器触发时传入的参数(未使用).
        """
        ...

    @classmethod
    def deinit(cls) -> None:
        """
        停止并释放当前使用的定时器资源.
        """
        ...

    @classmethod
    def is_running(cls) -> bool:
        """
        判断当前是否有任务正在运行.

        返回:
            (bool): 如果有任务在运行则返回 True,否则返回 False.
        """
        ...