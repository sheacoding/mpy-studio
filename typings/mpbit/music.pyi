"""
MicroPython music module for playing melodies.
This module provides functions for playing musical notes and built-in tunes.
"""

from typing import Union, Optional, List

# Built-in tunes (Western)
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

# Built-in tunes (Chinese Traditional)
GE_CHANG_ZU_GUO: bytes  # 歌唱祖国
DONG_FANG_HONG: bytes  # 东方红
CAI_YUN_ZHUI_YUE: bytes  # 彩云追月
ZOU_JIN_XIN_SHI_DAI: bytes  # 走进新时代
MO_LI_HUA: bytes  # 茉莉花
YI_MENG_SHAN_XIAO_DIAO: bytes  # 沂蒙山小调

def __init__() -> None:
    """
    Initialize the music module.
    """
    ...

def reset() -> None:
    """
    Reset the music module to its default state.
    """
    ...

def set_tempo(ticks: int = 4, bpm: int = 120) -> None:
    """
    Set the tempo for playback.

    Args:
        ticks: Number of ticks per beat (default: 4)
        bpm: Beats per minute (default: 120)
    """
    ...

def get_tempo() -> tuple[int, int]:
    """
    Get the current tempo settings.

    Returns:
        A tuple of (ticks, bpm)
    """
    ...

def play(music: Union[str, bytes, List[Union[str, int, float]]], pin: Optional[int] = None, wait: bool = True, loop: bool = False) -> None:
    """
    Play a melody.

    Args:
        music: The music to play. Can be a built-in tune, a string of notes, or a list of notes
        pin: Optional pin number to play on (default: None)
        wait: Whether to wait for the melody to finish (default: True)
        loop: Whether to loop the melody (default: False)
    """
    ...

def pitch(frequency: int, duration: Optional[int] = None, pin: Optional[int] = None, wait: bool = True) -> None:
    """
    Play a pitch at the specified frequency.

    Args:
        frequency: Frequency in Hz
        duration: Optional duration in milliseconds
        pin: Optional pin number to play on
        wait: Whether to wait for the pitch to finish playing
    """
    ...

def stop(pin: Optional[int] = None) -> None:
    """
    Stop playing music.

    Args:
        pin: Optional pin number to stop (default: None, stops all pins)
    """
    ...