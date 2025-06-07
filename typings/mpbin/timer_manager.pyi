from typing import Any, Callable, List, Optional, Tuple
from machine import Timer

class TimerManager:
    # Task type constants
    LOOP: int  # 循环执行
    ONCE: int  # 执行一次
    EXEC: int  # 立即执行

    # Time tolerance threshold (milliseconds)
    _TOLERANCE: int  # Acceptable execution time error range (±5ms)

    _tim: Optional[Timer]
    _tasks: List[Tuple[int, int, Callable[[Any], None], int]]  # [next_time, period, callback, task_type]
    _timer_id: Optional[int]

    @classmethod
    def _init(cls) -> None: ...

    @classmethod
    def loop(cls, period: int, cb: Callable[[Any], None]) -> None:
        """循环执行任务，每隔period毫秒执行一次"""
        ...

    @classmethod
    def delay(cls, period: int, cb: Callable[[Any], None]) -> None:
        """延迟执行任务，period毫秒后执行一次"""
        ...

    @classmethod
    def exec(cls, cb: Callable[[Any], None]) -> None:
        """立即执行任务，不计算时差"""
        ...

    @classmethod
    def remove(cls, cb: Callable[[Any], None]) -> None:
        """移除指定回调函数的任务"""
        ...

    @classmethod
    def _check(cls, _: Any) -> None:
        """检查并执行到期的任务"""
        ...

    @classmethod
    def deinit(cls) -> None:
        """停止定时器并清理资源"""
        ...

    @classmethod
    def is_running(cls) -> bool:
        """检查定时器是否正在运行"""
        ...