# typings/mpbit/educore/speaker.pyi
from typing import Optional, Union

class speaker:
    def __init__(self, pin: Optional[int] = None) -> None:
        """
        初始化一个扬声器对象

        参数:
            pin (Optional[int]): 外接扬声器连接的引脚编号。
                - 若为 None: 使用板载蜂鸣器
                - 若为 int: 表示使用指定引脚的外接扬声器
        """
        ...

    def tone(self, freq: Union[int, list] = 1000, dur: Optional[int] = None) -> None:
        """
        播放指定频率的声音

        参数:
            freq (Union[int, list]): 要播放的频率值或频率列表（若为列表取第一个值）
            dur (Optional[int]): 持续时间（单位：毫秒），若为 None 表示持续播放
        """
        ...

    def stop(self) -> None:
        """
        停止当前正在播放的声音
        """
        ...