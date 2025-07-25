from typing import Any, List, Optional

class Speaker:
    '''Speaker 音频播放类（MicroPython C模块）'''
    def __init__(
        self,
        *,
        i2s_num: int = 1,
        sck: int = 0,
        ws: int = 38,
        sd: int = 45,
        mck: int = 3,
        mode: int = 2,
        bits: int = 16,
        format: int = 0,
        rate: int = 16000,
        ibuf: int = 8192
    ) -> None: ...

    def play(self, filename: str, *, wait: bool = True) -> None:
        '''播放 WAV/MP3 文件，wait=True 阻塞，wait=False 后台播放'''
        ...

    def play_music(self, notes: List[str], *, wait: bool = True, bpm: int = 120) -> None:
        '''按音符序列合成方波音乐，支持 wait/bpm 参数'''
        ...

    def set_volume(self, volume: int) -> None:
        '''设置音量百分比 0-100'''
        ...

    def get_volume(self) -> int:
        '''获取当前音量百分比'''
        ...

    def deinit(self) -> None:
        '''释放 I2S 资源'''
        ... 