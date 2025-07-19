# Sentry.pyi

from typing import Tuple, List, Any, Optional

__version__: str  # 模块版本号.
__license__: str  # 许可证信息.

SENTRY_FIRMWARE_VERSION: int  # 固件版本号.
SENTRY_MAX_RESULT: int  # 支持的最大检测结果数量.

# 状态码定义.
SENTRY_OK: int  # 成功.
SENTRY_FAIL: int  # 失败.
SENTRY_WRITE_TIMEOUT: int  # 写入超时.
SENTRY_READ_TIMEOUT: int  # 读取超时.
SENTRY_CHECK_ERROR: int  # 校验错误.
SENTRY_UNSUPPORT_PARAM: int  # 不支持的参数.
SENTRY_UNKNOWN_PROTOCOL: int  # 协议未知.

# 协议错误类型.
SENTRY_PROTOC_OK: int  # 协议操作成功.
SENTRY_PROTOC_FAIL: int  # 协议操作失败.
SENTRY_PROTOC_UNKNOWN: int  # 未知协议.
SENTRY_PROTOC_TIMEOUT: int  # 协议超时.
SENTRY_PROTOC_CHECK_ERROR: int  # 校验错误.
SENTRY_PROTOC_LENGTH_ERROR: int  # 数据长度错误.
SENTRY_PROTOC_UNSUPPORT_COMMAND: int  # 不支持的命令.
SENTRY_PROTOC_UNSUPPORT_REG_ADDRESS: int  # 不支持的寄存器地址.
SENTRY_PROTOC_UNSUPPORT_REG_VALUE: int  # 不支持的寄存器值.
SENTRY_PROTOC_READ_ONLY: int  # 只读寄存器.
SENTRY_PROTOC_RESTART_ERROR: int  # 重启错误.
SENTRY_PROTOC_RESULT_NOT_END: int  # 结果未结束.

# 协议命令.
SENTRY_PROTOC_START: int  # 协议开始.
SENTRY_PROTOC_END: int  # 协议结束.
SENTRY_PROTOC_COMMADN_SET: int  # 设置命令.
SENTRY_PROTOC_COMMADN_GET: int  # 获取命令.
SENTRY_PROTOC_SET_PARAM: int  # 设置参数.
SENTRY_PROTOC_GET_RESULT: int  # 获取结果.
SENTRY_PROTOC_MESSAGE: int  # 消息类型.

# 寄存器地址定义.
kRegDeviceId: int  # 设备ID.
kRegFirmwareVersion: int  # 固件版本.
kRegRestart: int  # 重启控制.
kRegSensorConfig1: int  # 传感器配置1.
kRegLock: int  # 锁定寄存器.
kRegLed: int  # LED 控制.
kRegLedLevel: int  # LED 亮度.
kRegUart: int  # UART 配置.
kRegUSBCongig: int  # USB 配置.
kRegLcdCongig: int  # LCD 配置.
kRegHWConfig: int  # 硬件配置.
kRegCameraConfig1: int  # 相机配置1.
kRegCameraConfig2: int  # 相机配置2.
kRegCameraConfig3: int  # 相机配置3.
kRegCameraConfig4: int  # 相机配置4.
kRegCameraConfig5: int  # 相机配置5.
kRegFrameWidthH: int  # 帧宽高字节高位.
kRegFrameWidthL: int  # 帧宽低字节.
kRegFrameHeightH: int  # 帧高高位.
kRegFrameHeightL: int  # 帧高低位.
kRegFrameCount: int  # 帧计数.
kRegVisionId: int  # 视觉识别ID.
kRegVisionConfig1: int  # 视觉模块配置1.
kRegVisionConfig2: int  # 视觉模块配置2.
kRegParamNum: int  # 参数数量.
kRegParamId: int  # 参数ID.
kRegVisionStatus1: int  # 视觉状态1.
kRegVisionStatus2: int  # 视觉状态2.
kRegVisionDetect1: int  # 视觉检测状态1.
kRegVisionDetect2: int  # 视觉检测状态2.
kRegResultNumber: int  # 检测到的结果数量.
kRegResultId: int  # 结果ID.
kRegReadStatus1: int  # 读取状态1.
kRegParamValue1H: int  # 参数值1高位.
kRegParamValue1L: int  # 参数值1低位.
kRegParamValue2H: int  # 参数值2高位.
kRegParamValue2L: int  # 参数值2低位.
kRegParamValue3H: int  # 参数值3高位.
kRegParamValue3L: int  # 参数值3低位.
kRegParamValue4H: int  # 参数值4高位.
kRegParamValue4L: int  # 参数值4低位.
kRegParamValue5H: int  # 参数值5高位.
kRegParamValue5L: int  # 参数值5低位.
kRegResultData1H: int  # 结果数据1高位.
kRegResultData1L: int  # 结果数据1低位.
kRegResultData2H: int  # 结果数据2高位.
kRegResultData2L: int  # 结果数据2低位.
kRegResultData3H: int  # 结果数据3高位.
kRegResultData3L: int  # 结果数据3低位.
kRegResultData4H: int  # 结果数据4高位.
kRegResultData4L: int  # 结果数据4低位.
kRegResultData5H: int  # 结果数据5高位.
kRegResultData5L: int  # 结果数据5低位.
kRegSn: int  # 序列号寄存器.

# 对象信息字段定义.
class sentry_obj_info_e:
    kStatus: int
    """
    状态.
    """
    kXValue: int
    """
    X坐标.
    """
    kYValue: int
    """
    Y坐标.
    """
    kWidthValue: int
    """
    宽度.
    """
    kHeightValue: int
    """
    高度.
    """
    kLabel: int
    """
    标签.
    """
    kRValue: int
    """
    红色分量值.
    """
    kGValue: int
    """
    绿色分量值.
    """
    kBValue: int  
    """ 
    蓝色分量值.
    """

# 通信模式定义.
class sentry_mode_e:
    kSerialMode: int  # 串口模式.
    kI2CMode: int  # I2C 模式.
    kUnknownMode: int  # 未知模式.

# LED颜色定义.
class sentry_led_color_e:
    kLedClose: int  # 关闭LED.
    kLedRed: int  # 红色.
    kLedGreen: int  # 绿色.
    kLedYellow: int  # 黄色.
    kLedBlue: int  # 蓝色.
    kLedPurple: int  # 紫色.
    kLedCyan: int  # 青色.
    kLedWhite: int  # 白色.

# 波特率定义.
class sentry_baudrate_e:
    kBaud9600: int
    kBaud19200: int
    kBaud38400: int
    kBaud57600: int
    kBaud115200: int
    kBaud921600: int
    kBaud1152000: int
    kBaud2000000: int

# 相机缩放级别.
class sentry_camera_zoom_e:
    kZoomDefault: int  # 默认缩放.
    kZoom1: int  # 缩放等级1.
    kZoom2: int  # 缩放等级2.
    kZoom3: int  # 缩放等级3.
    kZoom4: int  # 缩放等级4.
    kZoom5: int  # 缩放等级5.

# 相机帧率设置.
class sentry_camera_fps_e:
    kFPSNormal: int  # 正常帧率.
    kFPSHigh: int  # 高帧率.

# 白平衡设置.
class sentry_camera_white_balance_e:
    kAutoWhiteBalance: int  # 自动白平衡.
    kLockWhiteBalance: int  # 锁定白平衡.
    kWhiteLight: int  # 白光.
    kYellowLight: int  # 黄光.
    kWhiteBalanceCalibrating: int  # 校准中.

# 颜色标签定义.
class color_label_e:
    kColorBlack: int  # 黑色.
    kColorWhite: int  # 白色.
    kColorRed: int  # 红色.
    kColorGreen: int  # 绿色.
    kColorBlue: int  # 蓝色.
    kColorYellow: int  # 黄色.

# 视觉识别类型 - Sentry1.
class sentry1_vision_e:
    kVisionColor: int  # 颜色识别.
    kVisionBlob: int  # 色块识别.
    kVisionBall: int  # 球体识别.
    kVisionLine: int  # 线条识别.
    kVisionCard: int  # 卡片识别.
    kVisionBody: int  # 人体识别.
    kVisionMaxType: int  # 最大类型.
    kVisionQrCode: int  # 二维码识别.
    kVisionMotionDetect: int  # 运动物体识别.

# 卡片标签 - Sentry1.
class sentry1_card_label_e:
    kCardForward: int  # 向前.
    kCardLeft: int  # 左转.
    kCardRight: int  # 右转.
    kCardTurnAround: int  # 掉头.
    kCardPark: int  # 停车.

# 球类标签 - Sentry1.
class sentry1_ball_label_e:
    kBallTableTennis: int  # 乒乓球.
    kBallTennis: int  # 网球.

# 形状卡片标签.
class sentry1_shape_card_e:
    kCardCheck: int  # √.
    kCardCross: int  # ×.
    kCardCircle: int  # 圆形.
    kCardSquare: int  # 方形.
    kCardTriangle: int  # 三角形.

# Sentry2视觉类型扩展.
class _sentry2_vision_e_out:
    kVision20Classes: int  # 20类物体识别.
    kVisionMotionDetect: int  # 运动检测.

# 视觉识别类型 - Sentry2.
class sentry2_vision_e(_sentry2_vision_e_out):
    kVisionColor: int
    """
    颜色识别.
    """
    kVisionBlob: int
    """
    色块识别.
    """
    kVisionAprilTag: int
    """
    标签识别.
    """
    kVisionLine: int 
    """
    线条识别.
    """
    kVisionLearning: int
    """
    深度学习.
    """
    kVisionCard: int
    """
    卡片识别.
    """
    kVisionFace: int
    """
    人脸识别.
    """
    kVision20Class: int
    """
    20类物体.
    """
    kVisionQrCode: int
    """
    二维码识别.
    """
    kVisionObjTrack: int
    """
    目标追踪.
    """
    kVisionMotion: int
    """
    动作检测.
    """
    kVisionCustom: int
    """
    自定义.
    """
    kVisionMaxType: int  
    """
    最大类型.
    """

# 卡片标签 - Sentry2.
class sentry2_card_label_e:
    kCardForward: int  # 向前.
    kCardLeft: int  # 左转.
    kCardRight: int  # 右转.
    kCardTurnAround: int  # 掉头.
    kCardPark: int  # 停车.
    kCardGreenLight: int  # 绿灯.
    kCardRedLight: int  # 红灯.
    kCardSpeed40: int  # 限速40.
    kCardSpeed60: int  # 限速60.
    kCardSpeed80: int  # 限速80.
    kCardCheck: int  # √.
    kCardCross: int  # ×.
    kCardCircle: int  # 圆形.
    kCardSquare: int  # 方形.
    kCardTriangle: int  # 三角形.
    kCardPlus: int  # 加号.
    kCardMinus: int  # 减号.
    kCardDivide: int  # 除号.
    kCardEqual: int  # 等于.
    kCardZero: int  # 数字0.
    kCardOne: int  # 数字1.
    kCardTwo: int  # 数字2.
    kCardThree: int  # 数字3.
    kCardFour: int  # 数字4.
    kCardFive: int  # 数字5.
    kCardSix: int  # 数字6.
    kCardSeven: int  # 数字7.
    kCardEight: int  # 数字8.
    kCardNine: int  # 数字9.
    kCardA: int  # 字母A.
    kCardB: int  # 字母B.
    kCardC: int  # 字母C.
    kCardD: int  # 字母D.
    kCardE: int  # 字母E.
    kCardF: int  # 字母F.
    kCardG: int  # 字母G.
    kCardH: int  # 字母H.
    kCardI: int  # 字母I.
    kCardJ: int  # 字母J.
    kCardK: int  # 字母K.
    kCardL: int  # 字母L.
    kCardM: int  # 字母M.
    kCardN: int  # 字母N.
    kCardO: int  # 字母O.
    kCardP: int  # 字母P.
    kCardQ: int  # 字母Q.
    kCardR: int  # 字母R.
    kCardS: int  # 字母S.
    kCardT: int  # 字母T.
    kCardU: int  # 字母U.
    kCardV: int  # 字母V.
    kCardW: int  # 字母W.
    kCardX: int  # 字母X.
    kCardY: int  # 字母Y.
    kCardZ: int  # 字母Z.

# 20类物体识别标签.
class class20_label_e:
    kAirplane: int  # 飞机.
    kBicycle: int  # 自行车.
    kBird: int  # 鸟.
    kBoat: int  # 船.
    kBottle: int  # 瓶子.
    kBus: int  # 公交车.
    kCar: int  # 小汽车.
    kCat: int  # 猫.
    kChair: int  # 椅子.
    kCow: int  # 牛.
    kTable: int  # 桌子.
    kDog: int  # 狗.
    kHorse: int  # 马.
    kMotorBike: int  # 摩托车.
    kPerson: int  # 人物.
    kPlant: int  # 植物.
    kSheep: int  # 羊.
    kSofa: int  # 沙发.
    kTrain: int  # 火车.
    kMonitor: int  # 显示器.

# 日志等级定义.
LOG_OFF: int
LOG_CRITICAL: int
LOG_ERROR: int
LOG_WARNING: int
LOG_INFO: int
LOG_DEBUG: int
LOG_NOTSET: int

# 日志记录类.
class SentryLogger:
    def __init__(self) -> None: ...
    def setLevel(self, level: int) -> None: ...  # 设置日志等级.
    def isEnabledFor(self, level: int) -> bool: ...  # 是否启用某等级日志.
    def log(self, name: str, level: int, msg: str, *args: Any) -> None: ...  # 记录日志.

# 检测结果类.
class result:
    result_data1: int  # 结果数据1.
    result_data2: int  # 结果数据2.
    result_data3: int  # 结果数据3.
    result_data4: int  # 结果数据4.
    result_data5: int  # 结果数据5.
    bytestr: str  # 字节字符串结果.

# 视觉状态类.
class VisionState:
    def __init__(self, vision_type: int) -> None: ...
    frame: int  # 当前帧编号.
    detect: int  # 检测状态.
    result: List[result]  # 检测结果列表.

# I2C通信接口类.
class SentryI2CMethod:
    def __init__(
        self,
        address: int,
        communication_port: Any,
        logger: Optional[SentryLogger] = None,
    ) -> None: ...
    def Logger(self, *arg: Any) -> None: ...  # 日志输出.
    def Set(self, reg_address: int, value: int) -> int: ...  # 写寄存器.
    def Get(self, reg_address: int) -> Tuple[int, int]: ...  # 读寄存器.
    def Read(
        self, vision_type: int, vision_state: VisionState
    ) -> Tuple[int, VisionState]: ...  # 读取视觉状态.
    def SetParam(
        self, vision_id: int, param: List[int], param_id: int
    ) -> int: ...  # 设置视觉参数.

# UART通信接口类.
class SentryUartMethod:
    def __init__(
        self,
        address: int,
        communication_port: Any,
        logger: Optional[SentryLogger] = None,
    ) -> None: ...
    def Logger(self, *arg: Any) -> None: ... # 日志输出.
    def Set(self, reg_address: int, value: int) -> int: ... # 写寄存器.
    def Get(self, reg_address: int) -> Tuple[int, int]: ... # 读寄存器.
    def Read(
        self, vision_type: int, vision_state: VisionState
    ) -> Tuple[int, VisionState]: ... # 读取视觉状态.
    def SetParam(self, vision_id: int, param: List[int], param_id: int) -> int: ... # 设置视觉参数.

# 基础设备类.
class SentryBase:
    def __init__(
        self, device_id: int, address: int = 0x60, log_level: int = LOG_ERROR
    ) -> None:
        """
        构造函数.

        参数:
            device_id (int): 设备ID.
            address (int): 设备地址(默认为0x60).
            log_level (int): 日志等级(默认为错误日志).
        """
        ...

    def Logger(self, *arg: Any) -> None: ...  # 输出日志.
    def SetDebug(self, log_level: int = LOG_OFF) -> None:
        """
        设置调试等级.

        参数:
            log_level (int): 日志等级,默认为 LOG_OFF.
            LOG_OFF (int): 关闭日志.
            LOG_CRITICAL (int): 致命错误日志.
            LOG_ERROR (int): 错误日志.
            LOG_WARNING (int): 警告日志.
            LOG_INFO (int): 信息日志.
            LOG_DEBUG (int): 调试日志.
            LOG_NOTSET (int): 日志等级未设置(通常用于表示未指定日志级别).
        """
        ...

    def begin(self, communication_port: Any = None) -> int:
        """
        启动设备.

        参数:
            communication_port: 通讯端口(I2C,UART).
        返回:
            (int): 状态码.
        """
        ...

    def VisionBegin(self, vision_type: int) -> int:
        """
        开启算法识别.

        参数:
            vision_type (int): 算法类型.
            - sentry2_vision_e.kVisionColor (int): 颜色识别.
            - sentry2_vision_e.kVisionBlob (int): 色块识别.
            - sentry2_vision_e.kVisionAprilTag (int): 标签识别.
            - sentry2_vision_e.kVisionLine (int): 线条识别.
            - sentry2_vision_e.kVisionLearning (int): 深度学习.
            - sentry2_vision_e.kVisionCard (int): 卡片识别.
            - sentry2_vision_e.kVisionFace (int): 人脸识别.
            - sentry2_vision_e.kVision20Class (int): 20类物体.
            - sentry2_vision_e.kVisionQrCode (int): 二维码识别.
            - sentry2_vision_e.kVisionObjTrack (int): 目标追踪.
            - sentry2_vision_e.kVisionMotion (int): 动作检测.
            - sentry2_vision_e.kVisionCustom (int): 自定义.

        返回:
            (int): 状态码.
        """
        ...

    def GetValue(
        self, vision_type: int, object_inf: int, obj_id: int = 1
    ) -> int: ...  # 获取对象属性.

    def SetParamNum(self, vision_type: int, max_num: int) -> int:
        """
        设置最大检测数.

        参数:
            vision_type (int): 识别类型.
            max_num (int): 最大检测数.
        """

        ...

    def SetParam(
        self, vision_type: int, param: List[int], param_id: int
    ) -> int:
        """
        设置算法参数.

        参数:
            vision_type (int): 识别类型.
            param (List[int]): 参数列表.
            param_id (int): 参数组索引.

        返回:
            (int): 状态码.
        """
        ...

    def GetVisionState(
        self, vision_type: int
    ) -> Optional[VisionState]: ...  # 获取视觉状态.

    def VisionSetStatus(
        self, vision_type: int, enable: bool
    ) -> int: ...  # 设置视觉开关.

    def VisionSetDefault(self, vision_type: int) -> int: ...  # 恢复默认设置.

    def VisionGetStatus(self, vision_type: int) -> int: ...  # 获取视觉是否开启.

    def UpdateResult(self, vision_type: int) -> int: ...  # 更新检测结果.

    def GetQrCodeValue(self) -> str: ...  # 获取二维码内容.

    def SensorSetRestart(self) -> int: ...  # 重启传感器.

    def SensorSetDefault(self) -> int: ...  # 传感器恢复出厂设置.

    def SeneorSetCoordinateType(self, coordinate: int) -> int: ...  # 设置坐标系统.

    def LedSetColor(
        self, detected_color: int, undetected_color: int, level: int
    ) -> int: ...  # 设置LED颜色.

    def LcdSetMode(self, on: bool) -> int: ...  # 设置LCD开关.

    def CameraSetZoom(self, zoom: int) -> int: ...  # 设置相机缩放.

    def CameraSetRotate(self, enable: bool) -> int: ...  # 设置图像旋转.

    def CameraSetFPS(self, fps: int) -> int: ...  # 设置帧率.

    def CameraSetAwb(self, awb: int) -> int: ...  # 设置白平衡.

    def CameraSetBrightness(self, Brightness: int) -> int: ...  # 设置亮度.

    def CameraSetContrast(self, Contrast: int) -> int: ...  # 设置对比度.

    def CameraSetSaturation(self, Saturation: int) -> int: ...  # 设置饱和度.

    def CameraSetShaprness(self, Shaprness: int) -> int: ...  # 设置清晰度.

    def CameraGetZoom(self) -> int: ...  # 获取当前缩放.

    def CameraGetAwb(self) -> int: ...  # 获取白平衡设置.

    def CameraGetRotate(self) -> int: ...  # 获取图像旋转状态.

    def CameraGetFPS(self) -> int: ...  # 获取当前帧率.

    def CameraGetBrightness(self) -> int: ...  # 获取亮度.

    def CameraGetContrast(self) -> int: ...  # 获取对比度.

    def CameraGetSaturation(self) -> int: ...  # 获取饱和度.

    def CameraGetShaprness(self, Shaprness: int) -> int: ...  # 获取清晰度.

    def UartSetBaudrate(self, baud: int) -> int: ...  # 设置UART波特率.

# Sentry1设备类.
class Sentry1(SentryBase):
    SENTRY1_DEVICE_ID: int  # 设备ID.
    def __init__(self, address: int = 0x60, log_level: int = LOG_ERROR) -> None: ...

# Sentry2设备类.
class Sentry2(SentryBase):
    SENTRY2_DEVICE_ID: int  # 设备ID.
    def __init__(self, address: int = 0x60, log_level: int = LOG_ERROR) -> None: ...
