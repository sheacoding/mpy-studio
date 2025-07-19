from typing import Optional, Callable

class button:
    a: str = "a"
    b: str = "b"

    def __init__(self, _type: str = "a") -> None:
        """
        初始化一个按钮对象.

        参数:
            _type (str): 按钮类型.
                - 'a' 表示板载按钮 A
                - 'b' 表示板载按钮 B
                - 其他值将尝试作为引脚编号int处理
        """

    @property
    def event_pressed(self) -> Optional[Callable[[], None]]:
        """
        获取当前的按下事件回调函数.

        返回:
            (Optional[Callable[[], None]]): 当前绑定的回调函数.
        """

    @event_pressed.setter
    def event_pressed(self, new_event_change: Optional[Callable[[], None]]) -> None:
        """
        设置按钮按下时触发的回调函数.

        参数:
            new_event_change (Optional[Callable[[], None]]): 新的回调函数.
                若为 None 则取消绑定.
        """

    def status(self) -> bool:
        """
        获取按钮当前状态.

        返回:
            (bool): True 表示按下,False 表示未按下.
        """