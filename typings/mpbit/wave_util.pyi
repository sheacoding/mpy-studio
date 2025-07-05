def create_wav_header(
    datasize: int, sample_rate: int, num_channels: int = 1, bits: int = 16
) -> bytearray:
    """
    生成标准WAV文件头.

    参数:
        datasize (int): 数据大小.
        sample_rate (int): 采样率.
        num_channels (int): 声道数,默认为1.
        bits (int): 位深度,默认为16.

    返回:
        (bytearray): WAV文件头数据.
    """
    ...
