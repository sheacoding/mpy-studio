from typing import Any, Callable, List, Optional, Tuple
from machine import Timer

class TimerManager:
    _tim: Optional[Timer]
    _tasks: List[Tuple[int, int, Callable[[Any], None], bool]]
    _timer_id: Optional[int]

    @classmethod
    def _init(cls) -> None: ...

    @classmethod
    def loop(cls, period: int, cb: Callable[[Any], None]) -> None: ...

    @classmethod
    def delay(cls, period: int, cb: Callable[[Any], None]) -> None: ...

    @classmethod
    def remove(cls, cb: Callable[[Any], None]) -> None: ...

    @classmethod
    def _check(cls, _: Any) -> None: ...

    @classmethod
    def deinit(cls) -> None: ...

    @classmethod
    def is_running(cls) -> bool: ...