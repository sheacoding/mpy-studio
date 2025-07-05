"""
Camera module type definitions for ESP32S3 MicroPython
基于 esp32-camera 驱动的 MicroPython 绑定
"""

from typing import List, Optional, Union, Any
from typing_extensions import Literal

# Enums
class FrameSize:
    """帧尺寸枚举"""
    QQVGA = 0      # 160x120
    QVGA = 6       # 320x240
    VGA = 7        # 640x480
    SVGA = 8       # 800x600
    XGA = 9        # 1024x768
    SXGA = 10      # 1280x1024
    UXGA = 11      # 1600x1200
    QXGA = 12      # 2048x1536
    HD = 13        # 1280x720
    FHD = 14       # 1920x1080
    QHD = 15       # 2560x1440
    QXGA2 = 16     # 2048x1080
    WQXGA = 17     # 2560x1600
    WQXGA2 = 18    # 2560x1440
    WQXGA3 = 19    # 2560x1080
    WQXGA4 = 20    # 2560x720
    WQXGA5 = 21    # 2560x640
    WQXGA6 = 22    # 2560x480
    WQXGA7 = 23    # 2560x360
    WQXGA8 = 24    # 2560x240
    WQXGA9 = 25    # 2560x120
    WQXGA10 = 26   # 2560x60

class PixelFormat:
    """像素格式枚举"""
    RGB565 = 0
    YUV422 = 1
    GRAYSCALE = 2
    JPEG = 3
    RGB555 = 4

class GainCeiling:
    """增益上限枚举"""
    GAINCEILING_2X = 0
    GAINCEILING_4X = 1
    GAINCEILING_8X = 2
    GAINCEILING_16X = 3
    GAINCEILING_32X = 4
    GAINCEILING_64X = 5
    GAINCEILING_128X = 6

class GrabMode:
    """抓取模式枚举"""
    WHEN_EMPTY = 0
    LATEST = 1

class Camera:
    """
    ESP32S3摄像头类
    参数:
        data_pins (List[int]) 8个数据引脚列表 [D0, D1, D2, D3, D4, D5, D6, D7]
        pclk_pin (int) 像素时钟引脚
        vsync_pin (int) 垂直同步引脚
        href_pin (int) 水平参考引脚
        sda_pin (int) SCCB SDA引脚
        scl_pin (int) SCCB SCL引脚
        xclk_pin (int) 外部时钟引脚
        xclk_freq (int) 外部时钟频率MHz 默认20
        pwdn_pin (int) 电源关闭引脚 默认-1
        reset_pin (int) 复位引脚 默认-1
        i2c_port (int) I2C端口号 默认0
        pixel_format (int) 像素格式 默认RGB565
        frame_size (int) 帧尺寸 默认QQVGA
        jpeg_quality (int) JPEG质量0-100 默认85
        fb_count (int) 帧缓冲区数量 默认2
        grab_mode (int) 抓取模式 默认WHEN_EMPTY
        init (bool) 构造时初始化摄像头 默认True
    返回:
        (None) 无返回值
    """
    
    def __init__(
        self,
        *,
        data_pins: Optional[List[int]] = None,
        pclk_pin: int,
        vsync_pin: int,
        href_pin: int,
        sda_pin: int,
        scl_pin: int,
        xclk_pin: int,
        xclk_freq: int = 20,
        pwdn_pin: int = -1,
        reset_pin: int = -1,
        i2c_port: int = 0,
        pixel_format: int = 1,
        frame_size: int = 0,
        jpeg_quality: int = 85,
        fb_count: int = 2,
        grab_mode: int = 0,
        init: bool = True
    ) -> None: ...
    
    # Main methods
    def capture(self) -> Optional[memoryview]:
        """
        捕获一帧图像数据
        参数:
            无
        返回:
            (memoryview) 捕获的帧数据
            (None) 没有可用帧时返回None
        """
        ...
    
    def frame_available(self) -> bool:
        """
        检查是否有可用帧
        参数:
            无
        返回:
            (bool) 有可用帧返回True 无可用帧返回False
        """
        ...
    
    def free_buffer(self) -> None:
        """
        释放当前帧缓冲区
        参数:
            无
        返回:
            (None) 无返回值
        """
        ...
    
    def init(self) -> None:
        """
        初始化摄像头
        参数:
            无
        返回:
            (None) 无返回值
        """
        ...
    
    def deinit(self) -> None:
        """
        反初始化摄像头
        参数:
            无
        返回:
            (None) 无返回值
        """
        ...
    
    def reconfigure(
        self,
        *,
        frame_size: Optional[int] = None,
        pixel_format: Optional[int] = None,
        grab_mode: Optional[int] = None,
        fb_count: Optional[int] = None
    ) -> None:
        """
        重新配置摄像头参数
        参数:
            frame_size (int) 新的帧尺寸
            pixel_format (int) 新的像素格式
            grab_mode (int) 新的抓取模式
            fb_count (int) 新的帧缓冲区数量
        返回:
            (None) 无返回值
        """
        ...
    
    # Context manager methods
    def __enter__(self) -> 'Camera': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def __del__(self) -> None: ...
    
    # Read-only properties
    @property
    def pixel_format(self) -> int:
        """
        获得像素格式
        返回:
            (int) 当前像素格式
        """
        ...
    
    @property
    def grab_mode(self) -> int:
        """
        获得抓取模式
        返回:
            (int) 当前抓取模式
        """
        ...
    
    @property
    def fb_count(self) -> int:
        """
        获得帧缓冲区数量
        返回:
            (int) 当前帧缓冲区数量
        """
        ...
    
    @property
    def pixel_width(self) -> int:
        """
        获得像素宽度
        返回:
            (int) 当前像素宽度
        """
        ...
    
    @property
    def pixel_height(self) -> int:
        """
        获得像素高度
        返回:
            (int) 当前像素高度
        """
        ...
    
    @property
    def max_frame_size(self) -> int:
        """
        获得最大支持的帧尺寸
        返回:
            (int) 最大帧尺寸
        """
        ...
    
    @property
    def sensor_name(self) -> str:
        """
        获得传感器名称
        返回:
            (str) 传感器名称
        """
        ...
    
    @property
    def supports_jpeg(self) -> bool:
        """
        是否支持JPEG
        返回:
            (bool) 支持返回True,不支持返回False
        """
        ...
    
    # Read-write properties
    @property
    def frame_size(self) -> int:
        """
        获得帧尺寸
        返回:
            (int) 当前帧尺寸
        """
        ...
    
    @frame_size.setter
    def frame_size(self, value: int) -> None:
        """
        设置帧尺寸
        参数:
            value (int) 新的帧尺寸
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def contrast(self) -> int:
        """
        获得对比度
        返回:
            (int) 当前对比度
        """
        ...
    
    @contrast.setter
    def contrast(self, value: int) -> None:
        """
        设置对比度
        参数:
            value (int) 新的对比度,范围-2到2
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def brightness(self) -> int:
        """
        获得亮度
        返回:
            (int) 当前亮度
        """
        ...
    
    @brightness.setter
    def brightness(self, value: int) -> None:
        """
        设置亮度
        参数:
            value (int) 新的亮度,范围-2到2
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def saturation(self) -> int:
        """
        获得饱和度
        返回:
            (int) 当前饱和度
        """
        ...
    
    @saturation.setter
    def saturation(self, value: int) -> None:
        """
        设置饱和度
        参数:
            value (int) 新的饱和度,范围-2到2
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def sharpness(self) -> int:
        """
        获得锐度
        返回:
            (int) 当前锐度
        """
        ...
    
    @sharpness.setter
    def sharpness(self, value: int) -> None:
        """
        设置锐度
        参数:
            value (int) 新的锐度,范围-2到2
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def denoise(self) -> int:
        """
        获得降噪设置
        返回:
            (int) 当前降噪设置
        """
        ...
    
    @denoise.setter
    def denoise(self, value: int) -> None:
        """
        设置降噪
        参数:
            value (int) 新的降噪设置,0或1
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def gainceiling(self) -> int:
        """
        获得增益上限
        返回:
            (int) 当前增益上限
        """
        ...
    
    @gainceiling.setter
    def gainceiling(self, value: int) -> None:
        """
        设置增益上限
        参数:
            value (int) 新的增益上限
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def quality(self) -> int:
        """
        获得JPEG质量
        返回:
            (int) 当前JPEG质量
        """
        ...
    
    @quality.setter
    def quality(self, value: int) -> None:
        """
        设置JPEG质量
        参数:
            value (int) 新的JPEG质量,范围0到100
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def colorbar(self) -> bool:
        """
        获得彩条测试模式
        返回:
            (bool) True为开启彩条,False为关闭
        """
        ...
    
    @colorbar.setter
    def colorbar(self, value: bool) -> None:
        """
        设置彩条测试模式
        参数:
            value (bool) True为开启彩条,False为关闭
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def whitebal(self) -> bool:
        """
        获得白平衡设置
        返回:
            (bool) True为自动白平衡,False为关闭
        """
        ...
    
    @whitebal.setter
    def whitebal(self, value: bool) -> None:
        """
        设置白平衡
        参数:
            value (bool) True为自动白平衡,False为关闭
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def gain_ctrl(self) -> bool:
        """
        获得增益控制设置
        返回:
            (bool) True为自动增益,False为关闭
        """
        ...
    
    @gain_ctrl.setter
    def gain_ctrl(self, value: bool) -> None:
        """
        设置增益控制
        参数:
            value (bool) True为自动增益,False为关闭
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def exposure_ctrl(self) -> bool:
        """
        获得曝光控制设置
        返回:
            (bool) True为自动曝光,False为关闭
        """
        ...
    
    @exposure_ctrl.setter
    def exposure_ctrl(self, value: bool) -> None:
        """
        设置曝光控制
        参数:
            value (bool) True为自动曝光,False为关闭
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def hmirror(self) -> bool:
        """
        获得水平镜像
        返回:
            (bool) True为水平镜像,False为正常
        """
        ...
    
    @hmirror.setter
    def hmirror(self, value: bool) -> None:
        """
        设置水平镜像
        参数:
            value (bool) True为水平镜像,False为正常
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def vflip(self) -> bool:
        """
        获得垂直翻转
        返回:
            (bool) True为垂直翻转,False为正常
        """
        ...
    
    @vflip.setter
    def vflip(self, value: bool) -> None:
        """
        设置垂直翻转
        参数:
            value (bool) True为垂直翻转,False为正常
        返回:
            (None) 无返回值
        """
        ...
    
    @property
    def aec2(self) -> bool:
        """Get AEC2 setting"""
        ...
    
    @aec2.setter
    def aec2(self, value: bool) -> None:
        """Set AEC2"""
        ...
    
    @property
    def awb_gain(self) -> bool:
        """Get AWB gain setting"""
        ...
    
    @awb_gain.setter
    def awb_gain(self, value: bool) -> None:
        """Set AWB gain"""
        ...
    
    @property
    def agc_gain(self) -> int:
        """Get AGC gain setting"""
        ...
    
    @agc_gain.setter
    def agc_gain(self, value: int) -> None:
        """Set AGC gain (0 to 30)"""
        ...
    
    @property
    def aec_value(self) -> int:
        """Get AEC value setting"""
        ...
    
    @aec_value.setter
    def aec_value(self, value: int) -> None:
        """Set AEC value (0 to 1200)"""
        ...
    
    @property
    def special_effect(self) -> int:
        """Get special effect setting"""
        ...
    
    @special_effect.setter
    def special_effect(self, value: int) -> None:
        """Set special effect (0 to 6)"""
        ...
    
    @property
    def wb_mode(self) -> int:
        """Get white balance mode setting"""
        ...
    
    @wb_mode.setter
    def wb_mode(self, value: int) -> None:
        """Set white balance mode (0 to 4)"""
        ...
    
    @property
    def ae_level(self) -> int:
        """Get AE level setting"""
        ...
    
    @ae_level.setter
    def ae_level(self, value: int) -> None:
        """Set AE level (-2 to 2)"""
        ...
    
    @property
    def dcw(self) -> bool:
        """Get DCW setting"""
        ...
    
    @dcw.setter
    def dcw(self, value: bool) -> None:
        """Set DCW"""
        ...
    
    @property
    def bpc(self) -> bool:
        """Get BPC setting"""
        ...
    
    @bpc.setter
    def bpc(self, value: bool) -> None:
        """Set BPC"""
        ...
    
    @property
    def wpc(self) -> bool:
        """Get WPC setting"""
        ...
    
    @wpc.setter
    def wpc(self, value: bool) -> None:
        """Set WPC"""
        ...
    
    @property
    def raw_gma(self) -> bool:
        """Get raw gamma setting"""
        ...
    
    @raw_gma.setter
    def raw_gma(self, value: bool) -> None:
        """Set raw gamma"""
        ...
    
    @property
    def lenc(self) -> bool:
        """Get lens correction setting"""
        ...
    
    @lenc.setter
    def lenc(self, value: bool) -> None:
        """Set lens correction"""
        ...

# Module level constants and types
__all__ = ['Camera', 'FrameSize', 'PixelFormat', 'GainCeiling', 'GrabMode'] 