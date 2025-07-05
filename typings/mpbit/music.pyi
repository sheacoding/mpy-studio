from typing import Union, Optional, List, Tuple

# 以下为内置西方曲调
DADADADUM: bytes
ENTERTAINER: bytes
PRELUDE: bytes
ODE: bytes
NYAN: bytes
RINGTONE: bytes
FUNK: bytes
BLUES: bytes
BIRTHDAY: bytes
WEDDING: bytes
FUNERAL: bytes
PUNCHLINE: bytes
PYTHON: bytes
BADDY: bytes
CHASE: bytes
BA_DING: bytes
WAWAWAWAA: bytes
JUMP_UP: bytes
JUMP_DOWN: bytes
POWER_UP: bytes
POWER_DOWN: bytes
# 以下为内置中国传统曲调
GE_CHANG_ZU_GUO: bytes  # 歌唱祖国.
DONG_FANG_HONG: bytes  # 东方红.
CAI_YUN_ZHUI_YUE: bytes  # 彩云追月.
ZOU_JIN_XIN_SHI_DAI: bytes  # 走进新时代.
MO_LI_HUA: bytes  # 茉莉花.
YI_MENG_SHAN_XIAO_DIAO: bytes  # 沂蒙山小调.

def __init__() -> None:
    """
    初始化音乐模块.
    """
    ...

def reset() -> None:
    """
    将音乐模块重置为默认状态.
    """
    ...

def set_tempo(ticks: int = 4, bpm: int = 120) -> None:
    """
    设置播放速度.

    参数:
        ticks (int): 每拍的节拍数(默认值:4).
        bpm (int): 每分钟节拍数(默认值:120).
    """
    ...

def get_tempo() -> Tuple[int, int]:
    """
    获取当前速度设置.

    返回:
        (Tuple[int, int]): 包含(ticks, bpm)的元组.
    """
    ...

def play(
    music: Union[str, bytes, List[Union[str, int, float]]],
    pin: Optional[int] = None,
    wait: bool = True,
    loop: bool = False,
) -> None:
    """
    播放旋律.

    参数:
        music (Union[str, bytes, List[Union[str, int, float]]]): 要播放的音乐.可以是内置曲调、音符字符串或音符列表.
        pin (Optional[int]): 可选的播放引脚编号(默认值:None).
        wait (bool): 是否等待旋律播放完成(默认值:True).
        loop (bool): 是否循环播放旋律(默认值:False).
    """
    ...

def pitch(
    frequency: int,
    duration: Optional[int] = None,
    pin: Optional[int] = None,
    wait: bool = True,
) -> None:
    """
    播放指定频率的音高.

    参数:
        frequency (int): 频率(单位:Hz).
        duration (Optional[int]): 可选的持续时间(单位:毫秒).
        pin (Optional[int]): 可选的播放引脚编号.
        wait (bool): 是否等待音高播放完成.
    """
    ...

def stop(pin: Optional[int] = None) -> None:
    """
    停止播放音乐.

    参数:
        pin (Optional[int]): 可选的停止引脚编号(默认值:None,停止所有引脚).
    """
    ...
