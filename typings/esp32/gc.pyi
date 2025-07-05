"""
控制垃圾回收器.

MicroPython模块: https://docs.micropython.org/en/v1.25.0/library/gc.html

CPython模块: :mod:`python:gc` https://docs.python.org/3/library/gc.html .

---
模块: 'gc' on micropython-v1.25.0-esp32-ESP32_GENERIC-SPIRAM
"""

# MCU: {'variant': 'SPIRAM', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC-SPIRAM', 'mpy': 'v6.3', 'ver': '1.25.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.25.0'}
# Stubber: v1.25.0
from __future__ import annotations
from _typeshed import Incomplete
from typing import overload
from typing_extensions import Awaitable, TypeAlias, TypeVar

def mem_alloc() -> int:
    """
    返回Python代码已分配的堆RAM字节数.

    提示:与CPython的差异
       :class: attention

       此函数是MicroPython扩展.
    """
    ...

def isenabled(*args, **kwargs) -> Incomplete: ...
def mem_free() -> int:
    """
    返回可供Python代码分配的堆RAM字节数,如果不知道这个数量,则返回-1.

    提示:与CPython的差异
       :class: attention

       此函数是MicroPython扩展.
    """
    ...

@overload
def threshold() -> int:
    """
    设置或查询额外的GC分配阈值. 通常情况下,只有当新的分配无法满足时才会触发回收,
    即在内存不足(OOM)的情况下. 如果调用此函数,除了OOM外,每次分配*amount*字节后
    (总计,自上次分配了这样数量的字节后)都会触发一次回收. *amount*通常指定为小于
    完整堆大小的值,目的是在堆耗尽之前提前触发回收,并希望提前回收能防止过度的内存碎片化.
    这是一种启发式措施,其效果将因应用程序而异,*amount*参数的最佳值也是如此.

    不带参数调用该函数将返回阈值的当前值. -1表示禁用分配阈值.

    提示:与CPython的差异
       :class: attention

       此函数是MicroPython扩展. CPython有一个类似的函数 - ``set_threshold()``,
       但由于GC实现不同,其签名和语义也不同.
    """

@overload
def threshold(amount: int) -> None:
    """
    设置或查询额外的GC分配阈值. 通常情况下,只有当新的分配无法满足时才会触发回收,
    即在内存不足(OOM)的情况下. 如果调用此函数,除了OOM外,每次分配*amount*字节后
    (总计,自上次分配了这样数量的字节后)都会触发一次回收. *amount*通常指定为小于
    完整堆大小的值,目的是在堆耗尽之前提前触发回收,并希望提前回收能防止过度的内存碎片化.
    这是一种启发式措施,其效果将因应用程序而异,*amount*参数的最佳值也是如此.

    不带参数调用该函数将返回阈值的当前值. -1表示禁用分配阈值.

    提示:与CPython的差异
       :class: attention

       此函数是MicroPython扩展. CPython有一个类似的函数 - ``set_threshold()``,
       但由于GC实现不同,其签名和语义也不同.
    """

def collect() -> None:
    """
    运行垃圾回收.
    """
    ...

def enable() -> None:
    """
    启用自动垃圾回收.
    """
    ...

def disable() -> None:
    """
    禁用自动垃圾回收. 仍然可以分配堆内存,
    并且仍然可以使用:meth:`gc.collect`手动启动垃圾回收.
    """
    ...
