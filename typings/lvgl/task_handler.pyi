# MIT license; Copyright (c) 2021 Amir Gonnen
# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Callable, ClassVar, Optional
from machine import Timer

_default_timer_id: int = ...


def _default_exception_hook(e: Exception):
    """
    默认异常处理钩子
    
    参数:
        e (Exception): 异常对象
    返回:
        (None): 无返回值
    """
    ...

##############################################################################

class TaskHandler(object):
    _current_instance: TaskHandler|None = ...

    duration: int = ...
    refresh_cb: Optional[Callable] = ...
    _timer: Timer = ...
    _task_handler_ref: Callable = ...

    exception_hook: Callable[[Exception], None] = ...
    max_scheduled: int = ...
    _scheduled: int = ...

    def __init__(
        self,
        duration: int = 33,
        timer_id: int = _default_timer_id,
        max_scheduled: int = 2,
        refresh_cb: Optional[Callable] = None,
        exception_hook: Callable[[Exception], None] = _default_exception_hook
    ):
        """
        初始化任务处理器
        
        参数:
            duration (int): 任务执行间隔毫秒数,默认33
            timer_id (int): 定时器ID,默认使用默认定时器
            max_scheduled (int): 最大调度任务数,默认2
            refresh_cb (Optional[Callable]): 刷新回调函数,默认None
            exception_hook (Callable[[Exception], None]): 异常处理钩子,默认使用默认钩子
        返回:
            (None): 无返回值
        """
        ...

    def deinit(self) -> None:
        """
        反初始化任务处理器
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def disable(self) -> None:
        """
        禁用任务处理器
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    def enable(self) -> None:
        """
        启用任务处理器
        
        参数:
            无
        返回:
            (None): 无返回值
        """
        ...

    @classmethod
    def is_running(cls) -> bool:
        """
        检查任务处理器是否正在运行
        
        参数:
            无
        返回:
            (bool): 是否正在运行
        """
        ...

    def _task_handler(self, _) -> None:
        """
        内部任务处理函数
        
        参数:
            _: 未使用的参数
        返回:
            (None): 无返回值
        """
        ...

    def _timer_cb(self, _) -> None:
        """
        内部定时器回调函数
        
        参数:
            _: 未使用的参数
        返回:
            (None): 无返回值
        """
        ...
