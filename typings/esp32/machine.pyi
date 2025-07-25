"""
与硬件相关的功能函数.

MicroPython模块: https://docs.micropython.org/en/v1.25.0/library/machine.html

``machine``模块包含与特定开发板硬件相关的功能函数.此模块中的大多数函数允许
直接且不受限制地访问和控制系统上的硬件块(如CPU、定时器、总线等).使用不当可能
导致开发板故障、锁死、崩溃,在极端情况下甚至可能导致硬件损坏.

---
模块: 'machine' on micropython-v1.25.0-esp32-ESP32_GENERIC-SPIRAM
"""

# MCU: {'variant': 'SPIRAM', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC-SPIRAM', 'mpy': 'v6.3', 'ver': '1.25.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.25.0'}
# Stubber: v1.25.0
from __future__ import annotations
from typing import (
    NoReturn,
    Optional,
    Union,
    Tuple,
    Any,
    Callable,
    List,
    Sequence,
    overload,
    Final,
)
from _typeshed import Incomplete
from typing_extensions import deprecated, Awaitable, TypeAlias, TypeVar
from _mpy_shed import _IRQ, AnyReadableBuf, AnyWritableBuf
from vfs import AbstractBlockDev


SLEEP: Final[int] = 2
DEEPSLEEP: Final[int] = 4

PWRON_RESET = 1
HARD_RESET = 2
WDT_RESET = 3
DEEPSLEEP_RESET = 4
SOFT_RESET = 5

PIN_WAKE = 2
EXT0_WAKE = 2
EXT1_WAKE = 3
TIMER_WAKE = 4
TOUCHPAD_WAKE =5
ULP_WAKE = 6

ATTN_0DB: int = ...
ID_T: TypeAlias = int | str
PinLike: TypeAlias = Pin | int | str
IDLE: Incomplete
WLAN_WAKE: Incomplete
RTC_WAKE: Incomplete

@overload
def deepsleep() -> NoReturn:
    """
    停止执行并尝试进入低功耗状态.

    如果指定了*time_ms*参数,则这将是睡眠持续的最大毫秒数.否则,睡眠可以无限期持续.

    无论是否有超时设置,如果有需要处理的事件,执行可能会随时恢复.这些事件或唤醒源
    应在睡眠前配置好,例如`Pin`变化或`RTC`超时.

    轻度睡眠和深度睡眠的精确行为和省电能力高度依赖于底层硬件,但一般特性如下:

    * 轻度睡眠(lightsleep)具有完整的RAM和状态保留.唤醒后,执行从请求睡眠的点恢复,
      所有子系统均可操作.

    * 深度睡眠(deepsleep)可能不保留RAM或系统的任何其他状态(例如外设或网络接口).
      唤醒后,执行从主脚本恢复,类似于硬复位或上电复位.`reset_cause()`函数将
      返回`machine.DEEPSLEEP`,可用于区分深度睡眠唤醒和其他复位.
    """

@overload
def deepsleep(time_ms: int, /) -> NoReturn:
    """
    停止执行并尝试进入低功耗状态.

    如果指定了*time_ms*参数,则这将是睡眠持续的最大毫秒数.否则,睡眠可以无限期持续.

    无论是否有超时设置,如果有需要处理的事件,执行可能会随时恢复.这些事件或唤醒源
    应在睡眠前配置好,例如`Pin`变化或`RTC`超时.

    轻度睡眠和深度睡眠的精确行为和省电能力高度依赖于底层硬件,但一般特性如下:

    * 轻度睡眠(lightsleep)具有完整的RAM和状态保留.唤醒后,执行从请求睡眠的点恢复,
      所有子系统均可操作.

    * 深度睡眠(deepsleep)可能不保留RAM或系统的任何其他状态(例如外设或网络接口).
      唤醒后,执行从主脚本恢复,类似于硬复位或上电复位.`reset_cause()`函数将
      返回`machine.DEEPSLEEP`,可用于区分深度睡眠唤醒和其他复位.
    """

def soft_reset() -> NoReturn:
    """
    执行解释器的:ref:`软复位 <soft_reset>`,删除所有Python对象并重置Python堆.
    """
    ...

def dht_readinto(*args, **kwargs) -> Incomplete: ...
def reset() -> NoReturn:
    """
    以类似于按下外部RESET按钮的方式:ref:`硬复位 <hard_reset>`设备.
    """
    ...

def unique_id() -> bytes:
    """
    返回一个包含开发板/SoC唯一标识符的字节字符串.如果底层硬件允许,它会在不同的
    开发板/SoC实例之间变化.长度因硬件而异(如果需要短ID,请使用完整值的子字符串).
    在某些MicroPython端口中,ID对应于网络MAC地址.
    """
    ...

def time_pulse_us(pin: Pin, pulse_level: int, timeout_us: int = 1_000_000, /) -> int:
    """
    测量给定引脚上的脉冲持续时间,并以微秒为单位返回结果.

    参数:
        pin (Pin): 要测量脉冲的引脚对象.
        pulse_level (int): 要测量的脉冲电平 (0=低电平脉冲,1=高电平脉冲).
        timeout_us (int): 超时时间,单位为微秒,默认为1,000,000微秒(1秒).

    返回值:
        (int): 脉冲持续时间(微秒),如果发生超时则返回负值.
             -1: 测量过程中超时.
             -2: 等待初始电平变化时超时.

    工作原理:
    1. 如果引脚当前电平与pulse_level不同,函数会等待直到电平变为pulse_level.
    2. 然后测量引脚保持在pulse_level电平的持续时间.
    3. 如果引脚已经处于pulse_level电平,则立即开始计时.
    """
    ...

def bitstream(pin, encoding, timing, data, /) -> Incomplete:
    """
    通过对指定的*pin*进行位操作传输*data*.*encoding*参数指定如何编码位,
    *timing*是特定于编码的时序规范.

    支持的编码有:

      - ``0``表示"高低"脉冲持续时间调制.这将以定时脉冲传输0和1位,从最高有效位开始.
        *timing*必须是格式为``(high_time_0, low_time_0, high_time_1, low_time_1)``
        的四元组纳秒值.例如,``(400, 850, 800, 450)``是WS2812 RGB LED在800kHz下
        的时序规范.

    时序精度因端口而异.在48MHz的Cortex M0上,最佳精度为+/- 120ns,但在更快的MCU
    (ESP8266, ESP32, STM32, Pyboard)上,精度将接近+/-30ns.

    ``注意:`` 对于控制WS2812/NeoPixel条带,请参阅:mod:`neopixel`模块获取更高级的API.
    """
    ...

def idle() -> None:
    """
    关闭CPU时钟,有助于在短时间或长时间内降低功耗.外设继续工作,执行在任何中断
    触发时恢复,或最多在CPU暂停一毫秒后恢复.

    建议在任何持续检查外部变化(即轮询)的紧密循环中调用此函数.这将减少功耗而不
    显著影响性能.要进一步降低功耗,请参阅:func:`lightsleep`、:func:`time.sleep()`
    和:func:`time.sleep_ms()`函数.
    """
    ...

@overload
def freq() -> int:
    """
    返回CPU频率,单位为赫兹.

    在某些端口上,还可以通过传入*hz*参数来设置CPU频率.
    """

@overload
def freq(hz: int, /) -> None:
    """
    返回CPU频率,单位为赫兹.

    在某些端口上,还可以通过传入*hz*参数来设置CPU频率.
    """

@overload
def freq(self) -> int:
    """
    返回CPU频率,单位为赫兹.

    在某些端口上,还可以通过传入*hz*参数来设置CPU频率.
    """

@overload
def freq(
    self,
    value: int,
    /,
) -> None:
    """
    返回CPU频率,单位为赫兹.

    在某些端口上,还可以通过传入*hz*参数来设置CPU频率.
    """

@overload
def lightsleep() -> None:
    """
    停止执行并尝试进入低功耗状态.

    如果指定了*time_ms*参数,则这将是睡眠持续的最大毫秒数.否则,睡眠可以无限期持续.

    无论是否有超时设置,如果有需要处理的事件,执行可能会随时恢复.这些事件或唤醒源
    应在睡眠前配置好,例如`Pin`变化或`RTC`超时.

    轻度睡眠和深度睡眠的精确行为和省电能力高度依赖于底层硬件,但一般特性如下:

    * 轻度睡眠(lightsleep)具有完整的RAM和状态保留.唤醒后,执行从请求睡眠的点恢复,
      所有子系统均可操作.

    * 深度睡眠(deepsleep)可能不保留RAM或系统的任何其他状态(例如外设或网络接口).
      唤醒后,执行从主脚本恢复,类似于硬复位或上电复位.`reset_cause()`函数将
      返回`machine.DEEPSLEEP`,可用于区分深度睡眠唤醒和其他复位.
    """

@overload
def lightsleep(time_ms: int, /) -> None:
    """
    停止执行并尝试进入低功耗状态.

    如果指定了*time_ms*参数,则这将是睡眠持续的最大毫秒数.否则,睡眠可以无限期持续.

    无论是否有超时设置,如果有需要处理的事件,执行可能会随时恢复.这些事件或唤醒源
    应在睡眠前配置好,例如`Pin`变化或`RTC`超时.

    轻度睡眠和深度睡眠的精确行为和省电能力高度依赖于底层硬件,但一般特性如下:

    * 轻度睡眠(lightsleep)具有完整的RAM和状态保留.唤醒后,执行从请求睡眠的点恢复,
      所有子系统均可操作.

    * 深度睡眠(deepsleep)可能不保留RAM或系统的任何其他状态(例如外设或网络接口).
      唤醒后,执行从主脚本恢复,类似于硬复位或上电复位.`reset_cause()`函数将
      返回`machine.DEEPSLEEP`,可用于区分深度睡眠唤醒和其他复位.
    """

def disable_irq() -> bool:
    """
    禁用中断请求.
    返回先前的IRQ状态,应将其视为不透明值.
    此返回值应传递给`enable_irq()`函数,以恢复中断到调用`disable_irq()`之前的原始状态.
    """
    ...

def enable_irq(state: bool = True, /) -> None:
    """
    重新启用中断请求.
    *state*参数应为从最近一次调用`disable_irq()`函数返回的值.
    """
    ...

def reset_cause() -> int:
    """
    获取复位原因.有关可能的返回值,请参阅:ref:`常量 <machine_constants>`.
    """
    ...

@deprecated("use :func:`lightsleep()` instead.")
def sleep() -> None:
    """
    ``注意:`` 此函数已弃用,请使用不带参数的:func:`lightsleep()`代替.
    """
    ...

def wake_reason() -> int:
    """
    获取唤醒原因.有关可能的返回值,请参阅:ref:`常量 <machine_constants>`.

    可用性: ESP32, WiPy.
    """
    ...

mem8: Incomplete  ## <class 'mem'> = <8-bit memory>

class PWM:
    """
    此类提供脉宽调制输出.

    使用示例::

        from machine import PWM

        pwm = PWM(pin)          # 在引脚上创建PWM对象.
        pwm.duty_u16(32768)     # 设置占空比为50%.

        # 重新初始化,周期为200us,占空比为5us.
        pwm.init(freq=5000, duty_ns=5000)

        pwm.duty_ns(3000)       # 设置脉冲宽度为3us.

        pwm.deinit()


    PWM的限制
    ------------------

    * 由于计算硬件的离散性质,不是所有频率都能以绝对精度生成.通常,PWM频率
      是通过将某个整数基频除以整数除数获得的.
      例如,如果基频为80MHz,所需PWM频率为300kHz,则除数必须是非整数
      80000000 / 300000 = 266.67.
      四舍五入后,除数设置为267,PWM频率将为80000000 / 267 = 299625.5 Hz,
      而不是300kHz.如果除数设置为266,则PWM频率将为80000000 / 266 = 300751.9 Hz,
      但仍然不是300kHz.

    * 占空比也具有相同的离散性质,无法达到其绝对精度.在大多数硬件平台上,
      占空比将在下一个频率周期应用.因此,在测量占空比之前,应等待超过"1/频率"的时间.

    * 频率和占空比分辨率通常是相互依赖的.PWM频率越高,可用的占空比分辨率越低,
      反之亦然.例如,300kHz的PWM频率可以有8位占空比分辨率,而不是可能预期的16位.
      在这种情况下,*duty_u16*的最低8位是不重要的.所以::

        pwm=PWM(Pin(13), freq=300_000, duty_u16=2**16//2)

      和::

        pwm=PWM(Pin(13), freq=300_000, duty_u16=2**16//2 + 255)

      将生成具有相同50%占空比的PWM.
    """

    @overload
    def duty_u16(self) -> int:
        """
        获取或设置PWM输出的当前占空比,作为0到65535(含)范围内的无符号16位值.

        不带参数时返回占空比.

        带有单个*value*参数时,将占空比设置为该值,以``value / 65535``的比率测量.
        """

    @overload
    def duty_u16(
        self,
        value: int,
        /,
    ) -> None:
        """
        获取或设置PWM输出的当前占空比,作为0到65535(含)范围内的无符号16位值.

        不带参数时返回占空比.

        带有单个*value*参数时,将占空比设置为该值,以``value / 65535``的比率测量.
        """

    def init(self, *, freq: int = ..., duty_u16: int = ..., duty_ns: int = ...) -> None:
        """
        修改PWM对象的设置.有关参数的详细信息,请参阅上面的构造函数.
        """
        ...

    @overload
    def freq(self) -> int:
        """
        获取或设置PWM输出的当前频率.

        不带参数时返回以Hz为单位的频率.

        带有单个*value*参数时,将频率设置为以Hz为单位的该值.如果频率超出有效范围,
        该方法可能会引发``ValueError``.
        """

    @overload
    def freq(
        self,
        value: int,
        /,
    ) -> None:
        """
        获取或设置PWM输出的当前频率.

        不带参数时返回以Hz为单位的频率.

        带有单个*value*参数时,将频率设置为以Hz为单位的该值.如果频率超出有效范围,
        该方法可能会引发``ValueError``.
        """

    def deinit(self) -> None:
        """
        禁用PWM输出.
        """
        ...

    @overload
    def duty_ns(self) -> int:
        """
        获取或设置PWM输出的当前脉冲宽度,以纳秒为单位.

        不带参数时返回以纳秒为单位的脉冲宽度.

        带有单个*value*参数时,将脉冲宽度设置为该值.
        """

    @overload
    def duty_ns(
        self,
        value: int,
        /,
    ) -> None:
        """
        获取或设置PWM输出的当前脉冲宽度,以纳秒为单位.

        不带参数时返回以纳秒为单位的脉冲宽度.

        带有单个*value*参数时,将脉冲宽度设置为该值.
        """

    def duty(self, *args, **kwargs) -> Incomplete: ...
    def __init__(
        self,
        dest: PinLike,
        /,
        *,
        freq: int = ...,
        duty_u16: int = ...,
        duty_ns: int = ...,
    ) -> None:
        """
        使用以下参数构造并返回一个新的PWM对象:

           - *dest*是输出PWM的实体,通常是一个:ref:`machine.Pin <machine.Pin>`对象,
             但某些端口可能允许其他值,如整数.
           - *freq*应为一个整数,设置PWM周期的频率,单位为Hz.
           - *duty_u16*设置占空比,比率为``duty_u16 / 65535``.
           - *duty_ns*设置脉冲宽度,单位为纳秒.

        设置*freq*可能会影响其他PWM对象,如果这些对象共享相同的底层PWM生成器(这取决于硬件).
        *duty_u16*和*duty_ns*一次只应指定其中一个.
        """

class UART:
    """
    UART实现了标准UART/USART全双工串行通信协议.在物理层面,
    它由2条线组成:RX和TX.通信单位是一个字符(不要与字符串字符混淆),
    可以是8位或9位宽.

    UART对象可以通过以下方式创建和初始化:

        from machine import UART

        uart = UART(1, 9600)                         # 使用给定波特率初始化.
        uart.init(9600, bits=8, parity=None, stop=1) # 使用给定参数初始化.

    支持的参数因开发板而异:

    Pyboard:位数可以是7、8或9.停止位可以是1或2.使用*parity=None*时,
    只支持8位和9位.启用奇偶校验时,只支持7位和8位.

    WiPy/CC3200:位数可以是5、6、7、8.停止位可以是1或2.

    UART对象的行为类似于`流`对象,读写操作使用标准流方法:

        uart.read(10)       # 读取10个字符,返回一个bytes对象.
        uart.read()         # 读取所有可用字符.
        uart.readline()     # 读取一行.
        uart.readinto(buf)  # 读取并存储到给定缓冲区.
        uart.write('abc')   # 写入3个字符.
    """

    INV_RX: Final[int] = 4
    INV_TX: Final[int] = 32
    INV_RTS: Final[int] = 64
    RTS: Final[int] = 1
    IRQ_RXIDLE: Final[int] = 4096
    IRQ_BREAK: Final[int] = 2
    IRQ_RX: Final[int] = 1
    INV_CTS: Final[int] = 8
    CTS: Final[int] = 2
    IRQ_TXIDLE: Incomplete
    IDLE: int = ...
    def irq(
        self,
        handler: Callable[[UART], None] | None = None,
        trigger: int = 0,
        hard: bool = False,
        /,
    ) -> _IRQ:
        """
        配置当UART事件发生时要调用的中断处理程序.

        参数如下:

          - *handler*是一个可选函数,在中断事件触发时调用.处理程序必须接受一个参数,
            即``UART``实例.

          - *trigger*配置可以生成中断的事件.可能的值是以下一个或多个的掩码:

            - ``UART.IRQ_RXIDLE`` 在接收至少一个字符后,RX线变为空闲状态时触发中断.
            - ``UART.IRQ_RX`` 在每个接收到的字符后触发中断.
            - ``UART.IRQ_TXIDLE`` 在消息的最后一个字符已发送或正在发送时触发中断.
            - ``UART.IRQ_BREAK`` 当在RX检测到中断状态时触发中断.

          - *hard*如果为true,则使用硬件中断.这减少了引脚变化与处理程序被调用之间的延迟.
            硬件中断处理程序可能不能分配内存;参见:ref:`isr_rules`.

        返回:
            (_IRQ): irq对象.

        由于硬件限制,并非所有触发事件在所有端口上都可用.
        """
        ...

    def sendbreak(self) -> None:
        """
        在总线上发送中断条件.这会使总线保持低电平状态,持续时间比正常字符传输所需的时间更长.
        """
        ...

    def deinit(self) -> None:
        """
        关闭UART总线.

        .. note::
          在调用``deinit()``后,您将无法在该对象上调用``init()``.
          在这种情况下,需要创建一个新的实例.
        """
        ...

    @overload
    def init(
        self,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        tx: PinLike | None = None,
        rx: PinLike | None = None,
        txbuf: int | None = None,
        rxbuf: int | None = None,
        timeout: int | None = None,
        timeout_char: int | None = None,
        invert: int | None = None,
    ) -> None:
        """
        使用给定参数初始化UART总线:

          - *baudrate*是时钟速率.
          - *bits*是每个字符的位数,7、8或9.
          - *parity*是奇偶校验,``None``、0(偶校验)或1(奇校验).
          - *stop*是停止位的数量,1或2.

        端口可能支持的其他仅关键字参数有:

          - *tx*指定要使用的TX引脚.
          - *rx*指定要使用的RX引脚.
          - *rts*指定用于硬件接收流控制的RTS(输出)引脚.
          - *cts*指定用于硬件发送流控制的CTS(输入)引脚.
          - *txbuf*指定TX缓冲区的字符长度.
          - *rxbuf*指定RX缓冲区的字符长度.
          - *timeout*指定等待第一个字符的时间(以毫秒为单位).
          - *timeout_char*指定字符之间等待的时间(以毫秒为单位).
          - *invert*指定要反转的线路.

              - ``0``不会反转线路(两条线路的空闲状态为逻辑高电平).
              - ``UART.INV_TX``将反转TX线(TX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_RX``将反转RX线(RX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_TX | UART.INV_RX``将反转两条线路(空闲状态为逻辑低电平).

          - *flow*指定要使用的硬件流控制信号.该值是一个位掩码.

              - ``0``将忽略硬件流控制信号.
              - ``UART.RTS``将启用接收流控制,通过使用RTS输出引脚来指示接收FIFO是否有足够空间接受更多数据.
              - ``UART.CTS``将启用发送流控制,当CTS输入引脚指示接收器缓冲区空间不足时暂停传输.
              - ``UART.RTS | UART.CTS``将同时启用两者,实现完全硬件流控制.

        在WiPy上,仅支持以下仅关键字参数:

          - *pins*是一个包含4个或2个项目的列表,指示TX、RX、RTS和CTS引脚(按此顺序).
            如果希望UART以有限功能运行,任何引脚都可以是None.

        .. note::
          可以在同一对象上多次调用``init()``,以重新配置UART,从而使用单个UART外设为不同的设备服务.
          仅在那种情况下不要调用``deinit()``,因为它会阻止再次调用``init()``.
        """

    @overload
    def init(
        self,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        pins: tuple[PinLike, PinLike] | None = None,
    ) -> None:
        """
        使用给定参数初始化UART总线:

          - *baudrate*是时钟速率.
          - *bits*是每个字符的位数,7、8或9.
          - *parity*是奇偶校验,``None``、0(偶校验)或1(奇校验).
          - *stop*是停止位的数量,1或2.

        端口可能支持的其他仅关键字参数有:

          - *tx*指定要使用的TX引脚.
          - *rx*指定要使用的RX引脚.
          - *rts*指定用于硬件接收流控制的RTS(输出)引脚.
          - *cts*指定用于硬件发送流控制的CTS(输入)引脚.
          - *txbuf*指定TX缓冲区的字符长度.
          - *rxbuf*指定RX缓冲区的字符长度.
          - *timeout*指定等待第一个字符的时间(以毫秒为单位).
          - *timeout_char*指定字符之间等待的时间(以毫秒为单位).
          - *invert*指定要反转的线路.

              - ``0``不会反转线路(两条线路的空闲状态为逻辑高电平).
              - ``UART.INV_TX``将反转TX线(TX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_RX``将反转RX线(RX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_TX | UART.INV_RX``将反转两条线路(空闲状态为逻辑低电平).

          - *flow*指定要使用的硬件流控制信号.该值是一个位掩码.

              - ``0``将忽略硬件流控制信号.
              - ``UART.RTS``将启用接收流控制,通过使用RTS输出引脚来指示接收FIFO是否有足够空间接受更多数据.
              - ``UART.CTS``将启用发送流控制,当CTS输入引脚指示接收器缓冲区空间不足时暂停传输.
              - ``UART.RTS | UART.CTS``将同时启用两者,实现完全硬件流控制.

        在WiPy上,仅支持以下仅关键字参数:

          - *pins*是一个包含4个或2个项目的列表,指示TX、RX、RTS和CTS引脚(按此顺序).
            如果希望UART以有限功能运行,任何引脚都可以是None.

        .. note::
          可以在同一对象上多次调用``init()``,以重新配置UART,从而使用单个UART外设为不同的设备服务.
          仅在那种情况下不要调用``deinit()``,因为它会阻止再次调用``init()``.
        """

    @overload
    def init(
        self,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        pins: tuple[PinLike, PinLike, PinLike, PinLike] | None = None,
    ) -> None:
        """
        使用给定参数初始化UART总线:

          - *baudrate*是时钟速率.
          - *bits*是每个字符的位数,7、8或9.
          - *parity*是奇偶校验,``None``、0(偶校验)或1(奇校验).
          - *stop*是停止位的数量,1或2.

        端口可能支持的其他仅关键字参数有:

          - *tx*指定要使用的TX引脚.
          - *rx*指定要使用的RX引脚.
          - *rts*指定用于硬件接收流控制的RTS(输出)引脚.
          - *cts*指定用于硬件发送流控制的CTS(输入)引脚.
          - *txbuf*指定TX缓冲区的字符长度.
          - *rxbuf*指定RX缓冲区的字符长度.
          - *timeout*指定等待第一个字符的时间(以毫秒为单位).
          - *timeout_char*指定字符之间等待的时间(以毫秒为单位).
          - *invert*指定要反转的线路.

              - ``0``不会反转线路(两条线路的空闲状态为逻辑高电平).
              - ``UART.INV_TX``将反转TX线(TX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_RX``将反转RX线(RX线的空闲状态现在为逻辑低电平).
              - ``UART.INV_TX | UART.INV_RX``将反转两条线路(空闲状态为逻辑低电平).

          - *flow*指定要使用的硬件流控制信号.该值是一个位掩码.

              - ``0``将忽略硬件流控制信号.
              - ``UART.RTS``将启用接收流控制,通过使用RTS输出引脚来指示接收FIFO是否有足够空间接受更多数据.
              - ``UART.CTS``将启用发送流控制,当CTS输入引脚指示接收器缓冲区空间不足时暂停传输.
              - ``UART.RTS | UART.CTS``将同时启用两者,实现完全硬件流控制.

        在WiPy上,仅支持以下仅关键字参数:

          - *pins*是一个包含4个或2个项目的列表,指示TX、RX、RTS和CTS引脚(按此顺序).
            如果希望UART以有限功能运行,任何引脚都可以是None.

        .. note::
          可以在同一对象上多次调用``init()``,以重新配置UART,从而使用单个UART外设为不同的设备服务.
          仅在那种情况下不要调用``deinit()``,因为它会阻止再次调用``init()``.
        """

    def flush(self) -> Incomplete:
        """
        等待所有数据发送完成.如果发生超时,将引发异常.超时时间取决于tx缓冲区大小和波特率.
        除非启用了流控制,否则不应该发生超时.

        .. note::

            对于esp8266和nrf端口,在最后一个字节发送时函数就会返回.
            如有需要,必须在调用脚本中添加一个字符的等待时间.

        可用性: rp2, esp32, esp8266, mimxrt, cc3200, stm32, nrf端口, renesas-ra
        """
        ...

    def txdone(self) -> bool:
        """
        判断所有数据是否已发送或没有数据传输正在进行.如果是这种情况,
        则返回``True``.如果数据传输正在进行中,则返回``False``.

        .. note::

            对于esp8266和nrf端口,即使传输的最后一个字节仍在发送,调用也可能返回``True``.
            如有需要,必须在调用脚本中添加一个字符的等待时间.

        可用性: rp2, esp32, esp8266, mimxrt, cc3200, stm32, nrf端口, renesas-ra
        """
        ...

    @overload
    def read(self) -> bytes | None:
        """
        读取字符.如果指定了``nbytes``,则最多读取那么多字节,
        否则读取尽可能多的数据.如果达到超时,可能会提前返回.
        超时在构造函数中可配置.

        返回值: 包含读取字节的bytes对象.超时时返回``None``.
        """

    @overload
    def read(self, nbytes: int, /) -> bytes | None:
        """
        读取字符.如果指定了``nbytes``,则最多读取那么多字节,
        否则读取尽可能多的数据.如果达到超时,可能会提前返回.
        超时在构造函数中可配置.

        返回值: 包含读取字节的bytes对象.超时时返回``None``.
        """

    def any(self) -> int:
        """
        返回一个整数,表示可以无阻塞读取的字符数.如果没有可用字符,将返回0;
        如果有字符可用,则返回正数.即使有多个字符可供读取,该方法也可能返回1.

        要更复杂地查询可用字符,请使用select.poll::

         poll = select.poll()
         poll.register(uart, select.POLLIN)
         poll.poll(timeout)
        """
        ...

    def write(self, buf: AnyReadableBuf, /) -> Union[int, None]:
        """
        将字节缓冲区写入总线.

        返回值: 写入的字节数或超时时返回``None``.
        """
        ...

    @overload
    def readinto(self, buf: AnyWritableBuf, /) -> int | None:
        """
        将字节读入``buf``.如果指定了``nbytes``,则最多读取那么多字节.
        否则,最多读取``len(buf)``字节.如果达到超时,可能会提前返回.
        超时在构造函数中可配置.

        返回值: 读取并存储到``buf``中的字节数,或超时时返回``None``.
        """

    @overload
    def readinto(self, buf: AnyWritableBuf, nbytes: int, /) -> int | None:
        """
        将字节读入``buf``.如果指定了``nbytes``,则最多读取那么多字节.
        否则,最多读取``len(buf)``字节.如果达到超时,可能会提前返回.
        超时在构造函数中可配置.

        返回值: 读取并存储到``buf``中的字节数,或超时时返回``None``.
        """

    def readline(self) -> Union[str, None]:
        """
        读取一行,以换行符结束.如果达到超时,可能会提前返回.
        超时在构造函数中可配置.

        返回值: 读取的行,或超时时返回``None``.
        """
        ...

    @overload
    def __init__(
        self,
        id: ID_T,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        tx: PinLike | None = None,
        rx: PinLike | None = None,
        txbuf: int | None = None,
        rxbuf: int | None = None,
        timeout: int | None = None,
        timeout_char: int | None = None,
        invert: int | None = None,
    ):
        """
        构造给定id的UART对象.
        """

    @overload
    def __init__(
        self,
        id: ID_T,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        pins: tuple[PinLike, PinLike] | None = None,
    ):
        """
        从两个引脚的元组构造给定id的UART对象.
        """

    @overload
    def __init__(
        self,
        id: ID_T,
        /,
        baudrate: int = 9600,
        bits: int = 8,
        parity: int | None = None,
        stop: int = 1,
        *,
        pins: tuple[PinLike, PinLike, PinLike, PinLike] | None = None,
    ):
        """
        从四个引脚的元组构造给定id的UART对象.
        """

mem32: Incomplete  ## <class 'mem'> = <32-bit memory>
mem16: Incomplete  ## <class 'mem'> = <16-bit memory>

class ADCBlock:
    """
    访问由*id*标识的ADC外设,*id*可以是整数或字符串.

    如果提供了*bits*参数,则设置转换过程的分辨率(以位为单位).
    如果未指定,则使用先前或默认分辨率.
    """

    def init(self, *, bits) -> None:
        """
        配置ADC外设.*bits*将设置转换过程的分辨率.
        """
        ...

    def connect(self, channel, source, *args, **kwargs) -> Incomplete:
        """
        连接ADC外设上的通道,使其准备好进行采样,
        并返回表示该连接的:ref:`ADC <machine.ADC>`对象.

        *channel*参数必须是整数,*source*必须是可以连接用于采样的对象
        (例如:ref:`Pin <machine.Pin>`)。

        如果只给定*channel*,则将其配置为采样.

        如果只给定*source*,则将该对象连接到默认通道,准备采样.

        如果同时给定*channel*和*source*,则将它们连接在一起,
        并准备好进行采样.

        任何额外的关键字参数都用于通过其:meth:`init <machine.ADC.init>`方法
        配置返回的ADC对象.
        """
        ...

    def __init__(self, id, *, bits) -> None: ...

class ADC:
    """
    ADC类提供了模数转换器的接口,代表一个可以对连续电压进行采样并
    将其转换为离散值的单一端点.

    使用示例::

       import machine

       adc = machine.ADC(pin)   # 创建一个作用于引脚的ADC对象.
       val = adc.read_u16()     # 读取0-65535范围内的原始模拟值.
    """

    ATTN_6DB: Final[int] = 2
    WIDTH_10BIT: Final[int] = 10
    WIDTH_11BIT: Final[int] = 11
    WIDTH_12BIT: Final[int] = 12
    WIDTH_9BIT: Final[int] = 9
    ATTN_0DB: Final[int] = 0
    ATTN_2_5DB: Final[int] = 1
    ATTN_11DB: Final[int] = 3
    VREF: int = ...
    CORE_VREF: int = ...
    CORE_VBAT: int = ...
    CORE_TEMP: int = ...
    def read_u16(self) -> int:
        """
        进行模拟读取并返回0-65535范围内的整数.
        返回值表示ADC获取的原始读数,经过缩放使得
        最小值为0,最大值为65535.
        """
        ...

    def init(self, *, sample_ns, atten) -> Incomplete:
        """
        将给定设置应用于ADC.只有指定的参数会被更改.
        有关参数的详细信息,请参阅上面的ADC构造函数.
        """
        ...

    def read_uv(self) -> int:
        """
        进行模拟读取并返回以微伏为单位的整数值.
        具体端口决定此值是否经过校准,以及如何进行校准.
        """
        ...

    def width(self, *args, **kwargs) -> Incomplete: ...
    def read(self, *args, **kwargs) -> Incomplete: ...
    def block(self) -> Incomplete:
        """
        返回与此ADC对象关联的:ref:`ADCBlock <machine.ADCBlock>`实例.

        此方法仅在端口支持:ref:`ADCBlock <machine.ADCBlock>`类时存在.
        """
        ...

    def atten(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, pin: PinLike, /) -> None:
        """
        访问与由*id*标识的源关联的ADC.这个
        *id*可以是整数(通常指定通道号)、
        :ref:`Pin <machine.Pin>`对象,或底层机器支持的其他值.
        .. note::

        WiPy有ADC的自定义实现,详情请参阅ADCWiPy.
        """

class I2S:
    """
    I2S是一种用于连接数字音频设备的同步串行协议.
    在物理层面,总线由3条线组成:SCK、WS、SD.
    I2S类支持控制器操作.不支持外设操作.

    I2S类目前作为技术预览版提供.在预览期间,鼓励用户提供反馈.
    基于这些反馈,I2S类API和实现可能会发生变化.

    I2S对象可以通过以下方式创建和初始化::

        from machine import I2S
        from machine import Pin

        # ESP32
        sck_pin = Pin(14)   # 串行时钟输出.
        ws_pin = Pin(13)    # 字时钟输出.
        sd_pin = Pin(12)    # 串行数据输出.

        或者

        # PyBoards
        sck_pin = Pin("Y6")   # 串行时钟输出.
        ws_pin = Pin("Y5")    # 字时钟输出.
        sd_pin = Pin("Y8")    # 串行数据输出.

        audio_out = I2S(2,
                        sck=sck_pin, ws=ws_pin, sd=sd_pin,
                        mode=I2S.TX,
                        bits=16,
                        format=I2S.MONO,
                        rate=44100,
                        ibuf=20000)

        audio_in = I2S(2,
                       sck=sck_pin, ws=ws_pin, sd=sd_pin,
                       mode=I2S.RX,
                       bits=32,
                       format=I2S.STEREO,
                       rate=22050,
                       ibuf=20000)

    支持3种操作模式:
     - 阻塞式.
     - 非阻塞式.
     - uasyncio.

    阻塞式::

       num_written = audio_out.write(buf) # 阻塞直到缓冲区清空.

       num_read = audio_in.readinto(buf) # 阻塞直到缓冲区填满.

    非阻塞式::

       audio_out.irq(i2s_callback)         # 当缓冲区清空时调用i2s_callback.
       num_written = audio_out.write(buf)  # 立即返回.

       audio_in.irq(i2s_callback)          # 当缓冲区填满时调用i2s_callback.
       num_read = audio_in.readinto(buf)   # 立即返回.

    uasyncio::

       swriter = uasyncio.StreamWriter(audio_out)
       swriter.write(buf)
       await swriter.drain()

       sreader = uasyncio.StreamReader(audio_in)
       num_read = await sreader.readinto(buf)
    """

    RX: Final[int] = 1
    MONO: Final[int] = 0
    STEREO: Final[int] = 1
    TX: Final[int] = 2
    @staticmethod
    def shift(
        buf: AnyWritableBuf,
        bits: int,
        shift: int,
        /,
    ) -> None:
        """
        对``buf``中包含的所有样本进行按位移位.``bits``指定样本大小(以位为单位).``shift``指定每个样本移位的位数.
        正值表示左移,负值表示右移.
        通常用于音量控制.每位移位改变样本音量6dB.
        """
        ...

    def init(
        self,
        *,
        sck: PinLike,
        ws: PinLike,
        sd: PinLike,
        mode: int,
        bits: int,
        format: int,
        rate: int,
        ibuf: int,
    ) -> None:
        """
        参见构造函数的参数描述.
        """
        ...

    def irq(
        self,
        handler: Callable[[], None],
        /,
    ) -> None:
        """
        设置回调函数.当``buf``被清空(``write``方法)或填满(``readinto``方法)时,调用``handler``.
        设置回调函数会将``write``和``readinto``方法更改为非阻塞操作.
        ``handler``在MicroPython调度程序的上下文中被调用.
        """
        ...

    def readinto(
        self,
        buf: AnyWritableBuf,
        /,
    ) -> int:
        """
        将音频样本读入由``buf``指定的缓冲区.``buf``必须支持缓冲协议,如bytearray或array.
        "buf"字节顺序为小端序.对于立体声格式,左声道样本在右声道样本之前.对于单声道格式,
        使用左声道样本数据.
        返回:
            (int): 读取的字节数.
        """
        ...

    def deinit(self) -> None:
        """
        Deinitialize the I2S bus.
        """
        ...

    def write(
        self,
        buf: AnyReadableBuf,
        /,
    ) -> int:
        """
        写入包含在 ``buf`` 中的音频样本.``buf``必须支持缓冲协议,如bytearray或array.
        "buf"字节顺序为小端序.对于立体声格式,左声道样本在右声道样本之前.对于单声道格式,
        样本数据会同时写入右声道和左声道.
        返回:
            (int): 写入的字节数.
        """
        ...

    def __init__(
        self,
        id: ID_T,
        /,
        *,
        sck: PinLike,
        ws: PinLike,
        sd: PinLike,
        mck: PinLike | None = None,
        mode: int,
        bits: int,
        format: int,
        rate: int,
        ibuf: int,
    ) -> None:
        """
        构造给定id的I2S对象:

        - ``id``标识特定的I2S总线.

        ``id``取决于开发板和端口:

          - PYBv1.0/v1.1: 有一个I2S总线,id=2.
          - PYBD-SFxW: 有两个I2S总线,id=1和id=2.
          - ESP32: 有两个I2S总线,id=0和id=1.

        所有端口都支持的仅关键字参数:

          - ``sck``是串行时钟线的引脚对象.
          - ``ws``是字选择线的引脚对象.
          - ``sd``是串行数据线的引脚对象.
          - ``mode``指定接收或发送.
          - ``bits``指定样本大小(位),16或32.
          - ``format``指定通道格式,STEREO或MONO.
          - ``rate``指定音频采样率(样本/秒).
          - ``ibuf``指定内部缓冲区长度(字节).

        对于所有端口,DMA在后台持续运行,允许用户应用程序在内部缓冲区和I2S外设单元之间传输样本数据的同时执行其他操作.
        增加内部缓冲区的大小可能会增加用户应用程序在下溢(例如``write``方法)或溢出(例如``readinto``方法)之前
        可以执行非I2S操作的时间.
        """

class DAC:
    def write(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, *argv, **kwargs) -> None: ...

class I2C:
    """
    I2C是一种用于设备间通信的双线协议

    它由2根线组成: SCL和SDA, 分别是时钟线和数据线

    I2C对象创建时会附加到特定的总线, 它们可以在创建时初始化, 也可以稍后初始化

    打印I2C对象会给出关于其配置的信息

    硬件和软件I2C实现都存在, 分别通过 `machine.I2C` 和 `machine.SoftI2C` 类提供
    硬件I2C使用系统的底层硬件支持来执行读/写操作, 通常高效快速, 但可能对可用引脚有限制
    软件I2C通过位操作实现, 可以在任何引脚上使用, 但效率较低
    这些类具有相同的可用方法, 主要区别在于它们的构造方式

    使用示例:
        from machine import I2C

        i2c = I2C(freq=400000)          # 以400kHz的频率创建I2C外设
                                        # 根据端口, 可能需要额外参数
                                        # 来选择要使用的外设和/或引脚

        i2c.scan()                      # 扫描外设, 返回7位地址列表

        i2c.writeto(42, b'123')         # 向7位地址为42的外设写入3个字节
        i2c.readfrom(42, 4)             # 从7位地址为42的外设读取4个字节

        i2c.readfrom_mem(42, 8, 3)      # 从外设42的内存中读取3个字节,
                                        # 从外设中的内存地址8开始
        i2c.writeto_mem(42, 2, b'\x10') # 向外设42的内存写入1个字节,
                                        # 从外设中的地址2开始
    """

    def readfrom_mem_into(
        self, addr: int, memaddr: int, buf: AnyWritableBuf, /, *, addrsize: int = 8
    ) -> None:
        """
        从指定地址的外设读取数据到缓冲区中

        参数:
            addr (int): 外设的7位地址
            memaddr (int): 内存地址
            buf (AnyWritableBuf): 用于接收读取数据的缓冲区
            addrsize (int): 地址大小 默认为8位

        返回:
            (None): 无返回值
        """
        ...

    def readfrom_into(
        self, addr: int, buf: AnyWritableBuf, stop: bool = True, /
    ) -> None:
        """
        从指定地址的外设读取数据到缓冲区中

        参数:
            addr (int): 外设的7位地址
            buf (AnyWritableBuf): 用于接收读取数据的缓冲区
            stop (bool): 传输结束时是否生成STOP条件 默认为True

        返回:
            (None): 无返回值
        """
        ...

    def readfrom_mem(
        self, addr: int, memaddr: int, nbytes: int, /, *, addrsize: int = 8
    ) -> bytes:
        """
        从指定地址的外设内存中读取字节

        参数:
            addr (int): 外设的7位地址
            memaddr (int): 内存地址
            nbytes (int): 要读取的字节数
            addrsize (int): 地址大小 默认为8位

        返回:
            (bytes): 包含读取数据的bytes对象
        """
        ...

    def writeto_mem(
        self, addr: int, memaddr: int, buf: AnyReadableBuf, /, *, addrsize: int = 8
    ) -> None:
        """
        将缓冲区中的数据写入指定地址的外设内存中

        参数:
            addr (int): 外设的7位地址
            memaddr (int): 内存地址
            buf (AnyReadableBuf): 包含要写入数据的缓冲区
            addrsize (int): 地址大小 默认为8位

        返回:
            (None): 无返回值
        """
        ...

    def scan(
        self,
    ) -> List:
        """
        扫描I2C总线上所有响应的设备地址

        返回:
            (List): 响应的7位地址列表
        """
        ...

    def writeto(self, addr: int, buf: AnyReadableBuf, stop: bool = True, /) -> int:
        """
        将缓冲区中的字节写入指定地址的外设

        参数:
            addr (int): 外设的7位地址
            buf (AnyReadableBuf): 包含要写入字节的缓冲区
            stop (bool): 传输结束时是否生成STOP条件 默认为True

        返回:
            (int): 收到ACK的数量
        """
        ...

    def writevto(
        self, addr: int, vector: Sequence[AnyReadableBuf], stop: bool = True, /
    ) -> int:
        """
        将向量中包含的字节写入指定地址的外设

        参数:
            addr (int): 外设的7位地址
            vector (Sequence[AnyReadableBuf]): 包含缓冲协议对象的元组或列表
            stop (bool): 传输结束时是否生成STOP条件 默认为True

        返回:
            (int): 收到ACK的数量
        """
        ...

    def start(self) -> None:
        """
        在总线上生成START条件(当SCL为高电平时,SDA转换为低电平).
        """
        ...

    def readfrom(self, addr: int, nbytes: int, stop: bool = True, /) -> bytes:
        """
        从指定的*addr*外设读取*nbytes*字节.
        如果*stop*为true,则在传输结束时生成STOP条件.
        返回:
            (bytes): 包含读取数据的`bytes`对象.
        """
        ...

    def readinto(self, buf: AnyWritableBuf, nack: bool = True, /) -> None:
        """
        从总线读取字节并将它们存储到*buf*中.读取的字节数是*buf*的长度.
        在接收除最后一个字节外的所有字节后,将在总线上发送ACK.
        接收到最后一个字节后,如果*nack*为true,则发送NACK,否则发送ACK
        (在这种情况下,外设假定在稍后的调用中将读取更多字节).
        """
        ...

    @overload
    def init(self, *, freq: int = 400_000) -> None:
        """
        Initialise the I2C bus with the given arguments:

           - *scl* is a pin object for the SCL line
           - *sda* is a pin object for the SDA line
           - *freq* is the SCL clock rate

         In the case of hardware I2C the actual clock frequency may be lower than the
         requested frequency. This is dependent on the platform hardware. The actual
         rate may be determined by printing the I2C object.
        """

    @overload
    def init(self, *, scl: PinLike, sda: PinLike, freq: int = 400_000) -> None:
        """
        使用给定参数初始化I2C总线:

           - *scl*是SCL线的引脚对象.
           - *sda*是SDA线的引脚对象.
           - *freq*是SCL时钟频率.

         在硬件I2C的情况下,实际时钟频率可能低于请求的频率.这取决于平台硬件.
         可以通过打印I2C对象来确定实际速率.
        """

    def stop(self) -> None:
        """
        在总线上生成STOP条件(当SCL为高电平时,SDA转换为高电平).
        """
        ...

    def write(self, buf: AnyReadableBuf, /) -> int:
        """
        将*buf*中的字节写入总线.在每个字节后检查是否收到ACK,
        如果收到NACK则停止发送剩余字节.
        返回:
            (int): 收到的ACK数量.
        """
        ...

    @overload
    def __init__(self, id: ID_T, /, *, freq: int = 400_000):
        """
        使用以下参数构造并返回新的I2C对象:

           - *id*标识特定的I2C外设.允许的值取决于特定的端口/开发板.
           - *scl*应该是指定用于SCL的引脚对象.
           - *sda*应该是指定用于SDA的引脚对象.
           - *freq*应该是一个整数,设置SCL的最大频率.

        注意,某些端口/开发板将有*scl*和*sda*的默认值,
        可以在此构造函数中更改.其他端口/开发板将有固定的
        *scl*和*sda*值,不能更改.
        """

    @overload
    def __init__(self, id: ID_T, /, *, scl: PinLike, sda: PinLike, freq: int = 400_000):
        """
        使用以下参数构造并返回新的I2C对象:

           - *id*标识特定的I2C外设.允许的值取决于特定的端口/开发板.
           - *scl*应该是指定用于SCL的引脚对象.
           - *sda*应该是指定用于SDA的引脚对象.
           - *freq*应该是一个整数,设置SCL的最大频率.

        注意,某些端口/开发板将有*scl*和*sda*的默认值,
        可以在此构造函数中更改.其他端口/开发板将有固定的
        *scl*和*sda*值,不能更改.
        """

    @overload
    def __init__(self, *, scl: PinLike, sda: PinLike, freq: int = 400_000) -> None:
        """
        使用给定参数初始化I2C总线:

           - *scl*是SCL线的引脚对象.
           - *sda*是SDA线的引脚对象.
           - *freq*是SCL时钟频率.

         在硬件I2C的情况下,实际时钟频率可能低于请求的频率.这取决于平台硬件.
         可以通过打印I2C对象来确定实际速率.
        """

    @overload
    def __init__(self, id: ID_T, /, *, freq: int = 400_000):
        """
        使用以下参数构造并返回新的I2C对象:

           - *id*标识特定的I2C外设.允许的值取决于特定的端口/开发板.
           - *scl*应该是指定用于SCL的引脚对象.
           - *sda*应该是指定用于SDA的引脚对象.
           - *freq*应该是一个整数,设置SCL的最大频率.

        注意,某些端口/开发板将有*scl*和*sda*的默认值,
        可以在此构造函数中更改.其他端口/开发板将有固定的
        *scl*和*sda*值,不能更改.
        """

    @overload
    def __init__(self, id: ID_T, /, *, scl: PinLike, sda: PinLike, freq: int = 400_000):
        """
        使用以下参数构造并返回新的I2C对象:

           - *id*标识特定的I2C外设.允许的值取决于特定的端口/开发板.
           - *scl*应该是指定用于SCL的引脚对象.
           - *sda*应该是指定用于SDA的引脚对象.
           - *freq*应该是一个整数,设置SCL的最大频率.

        注意,某些端口/开发板将有*scl*和*sda*的默认值,
        可以在此构造函数中更改.其他端口/开发板将有固定的
        *scl*和*sda*值,不能更改.
        """

    @overload
    def __init__(self, *, scl: PinLike, sda: PinLike, freq: int = 400_000) -> None:
        """
        使用给定参数初始化I2C总线:

           - *scl*是SCL线的引脚对象.
           - *sda*是SDA线的引脚对象.
           - *freq*是SCL时钟频率.

         在硬件I2C的情况下,实际时钟频率可能低于请求的频率.这取决于平台硬件.
         可以通过打印I2C对象来确定实际速率.
        """

class Timer:
    """
    硬件定时器处理周期和事件的计时.定时器可能是MCU和SoC中
    最灵活和最多样化的硬件类型,不同型号之间差异很大.MicroPython的Timer类
    定义了一个基本操作,即以给定周期执行回调(或在某个延迟后执行一次),
    并允许特定开发板定义更多非标准行为(因此不可移植到其他开发板).

    请参阅关于Timer回调的:ref:`重要限制 <machine_callbacks>`的讨论.

    .. note::

        内存不能在irq处理程序(中断)内分配,因此
        在处理程序中引发的异常不会提供太多信息.请参阅
        :func:`micropython.alloc_emergency_exception_buf`了解如何解决这个
        限制.

    如果您使用的是WiPy开发板,请参考:ref:`machine.TimerWiPy <machine.TimerWiPy>`
    而不是此类.
    """

    ONE_SHOT: Final[int] = 0
    PERIODIC: Final[int] = 1
    def deinit(self) -> None:
        """
        反初始化定时器.停止定时器,并禁用定时器外设.
        """
        ...

    @overload
    def init(
        self,
        *,
        mode: int = PERIODIC,
        period: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ) -> None: ...
    @overload
    def init(
        self,
        *,
        mode: int = PERIODIC,
        freq: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ) -> None: ...
    @overload
    def init(
        self,
        *,
        mode: int = PERIODIC,
        tick_hz: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ) -> None:
        """
        初始化定时器.示例::

            def mycallback(t):
                pass

            # 以1kHz周期运行.
            tim.init(mode=Timer.PERIODIC, freq=1000, callback=mycallback)

            # 周期为100ms.
            tim.init(period=100, callback=mycallback)

            # 1000ms后触发一次.
            tim.init(mode=Timer.ONE_SHOT, period=1000, callback=mycallback)

        关键字参数:

          - ``mode``可以是以下之一:

            - ``Timer.ONE_SHOT`` - 定时器运行一次,直到配置的
              通道周期到期.
            - ``Timer.PERIODIC`` - 定时器以配置的频率
              周期性运行.

          - ``freq`` - 定时器频率,单位为Hz.频率的上限
            取决于端口.当同时给出``freq``和``period``
            参数时,``freq``具有更高的优先级,``period``将被忽略.

          - ``period`` - 定时器周期,单位为毫秒.

          - ``callback`` - 定时器周期到期时要调用的可调用对象.
            回调必须接受一个参数,即传递的Timer对象.
            必须指定``callback``参数.否则在定时器到期时
            会发生异常:
            ``TypeError: 'NoneType' object isn't callable``
        """
        ...

    def value(self, *args, **kwargs) -> Incomplete: ...
    @overload
    def __init__(self, id: int, /):
        """
        构造给定``id``的新定时器对象.``id``为-1构造
        虚拟定时器(如果开发板支持).
        ``id``不应作为关键字参数传递.

        有关初始化参数,请参见``init``.
        """

    @overload
    def __init__(
        self,
        id: int,
        /,
        *,
        mode: int = PERIODIC,
        period: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ):
        """
        构造给定``id``的新定时器对象.``id``为-1构造
        虚拟定时器(如果开发板支持).
        ``id``不应作为关键字参数传递.

        有关初始化参数,请参见``init``.
        """

    @overload
    def __init__(
        self,
        id: int,
        /,
        *,
        mode: int = PERIODIC,
        freq: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ):
        """
        构造给定``id``的新定时器对象.``id``为-1构造
        虚拟定时器(如果开发板支持).
        ``id``不应作为关键字参数传递.

        有关初始化参数,请参见``init``.
        """

    @overload
    def __init__(
        self,
        id: int,
        /,
        *,
        mode: int = PERIODIC,
        tick_hz: int | None = None,
        callback: Callable[[Timer], None] | None = None,
    ):
        """
        构造给定``id``的新定时器对象.``id``为-1构造
        虚拟定时器(如果开发板支持).
        ``id``不应作为关键字参数传递.

        有关初始化参数,请参见``init``.
        """

class SoftSPI(SPI):
    """
    构造一个新的软件SPI对象.必须提供额外的参数,
    通常至少包括*sck*、*mosi*和*miso*,这些参数用于
    初始化总线.有关参数的描述,请参见`SPI.init`.
    """

    # LSB: Final[int] = 1
    # MSB: Final[int] = 0
    def deinit(self, *args, **kwargs) -> Incomplete: ...
    def init(self, *args, **kwargs) -> Incomplete: ...
    def write_readinto(self, *args, **kwargs) -> Incomplete: ...
    def read(self, *args, **kwargs) -> Incomplete: ...
    def write(self, *args, **kwargs) -> Incomplete: ...
    def readinto(self, *args, **kwargs) -> Incomplete: ...
    def __init__(
        self,
        baudrate=500000,
        *,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=SPI.MSB,
        sck: PinLike | None = None,
        mosi: PinLike | None = None,
        miso: PinLike | None = None,
    ) -> None: ...

class Pin:
    """
    引脚对象用于控制I/O引脚(也称为GPIO - 通用输入/输出).
    引脚对象通常与物理引脚相关联,该物理引脚可以驱动输出电压
    并读取输入电压.引脚类有设置引脚模式(IN、OUT等)的方法,
    以及获取和设置数字逻辑电平的方法.
    对于引脚的模拟控制,请参见:class:`ADC`类.

    引脚对象通过使用明确指定某个I/O引脚的标识符来构造.
    标识符的允许形式和标识符映射到的物理引脚是特定于端口的.
    标识符的可能形式有整数、字符串或带有端口和引脚号的元组.

    使用模型::

        from machine import Pin

        # 在引脚#0上创建一个输出引脚.
        p0 = Pin(0, Pin.OUT)

        # 将值设置为低电平然后高电平.
        p0.value(0)
        p0.value(1)

        # 在引脚#2上创建一个带上拉电阻的输入引脚.
        p2 = Pin(2, Pin.IN, Pin.PULL_UP)

        # 读取并打印引脚值.
        print(p2.value())

        # 重新配置引脚#0为带下拉电阻的输入模式.
        p0.init(p0.IN, p0.PULL_DOWN)

        # 配置中断回调.
        p0.irq(lambda p:print(p))
    """

    P0 = 33
    P1 = 32
    P2 = 35
    P3 = 34
    P4 = 39
    P5 = 0
    P6 = 16
    P7 = 17
    P8 = 26
    P9 = 25
    P10 = 36
    P11 = 2
    P13 = 18
    P14 = 19
    P15 = 21
    P16 = 5
    P19 = 22
    P20 = 23
    P23 = 27
    P24 = 14
    P25 = 12
    P26 = 13
    P27 = 15
    P28 = 4

    OPEN_DRAIN: Final[int] = 7
    OUT: Final[int] = 3
    IRQ_RISING: Final[int] = 1
    WAKE_LOW: Final[int] = 4
    WAKE_HIGH: Final[int] = 5
    PULL_DOWN: Final[int] = 1
    PULL_UP: Final[int] = 2
    DRIVE_1: Final[int] = 1
    IRQ_FALLING: Final[int] = 2
    DRIVE_0: Final[int] = 0
    IN: Final[int] = 1
    DRIVE_2: Final[int] = 2
    DRIVE_3: Final[int] = 3
    ALT: Incomplete
    ALT_OPEN_DRAIN: Incomplete
    ANALOG: Incomplete
    PULL_HOLD: Incomplete
    IRQ_LOW_LEVEL: Incomplete
    IRQ_HIGH_LEVEL: Incomplete
    def off(self) -> None:
        """
        将引脚设置为"0"输出电平.
        """
        ...

    def irq(
        self,
        /,
        handler: Callable[[Pin], None] | None = None,
        trigger: int = (IRQ_FALLING | IRQ_RISING),
        *,
        priority: int = 1,
        wake: int | None = None,
        hard: bool = False,
    ) -> Callable[..., Incomplete]:
        """
           配置在引脚的触发源处于活动状态时要调用的中断处理程序.如果引脚模式是``Pin.IN``,
           则触发源是引脚上的外部值.如果引脚模式是``Pin.OUT``,则触发源是引脚的输出缓冲区.
           否则,如果引脚模式是``Pin.OPEN_DRAIN``,则触发源在状态'0'时是输出缓冲区,
           在状态'1'时是外部引脚值.

           参数如下:

             - ``handler`` (Callable[[Pin], None] | None): 是一个可选函数,在中断触发时调用.处理程序必须接受一个参数,
               即``Pin``实例.

             - ``trigger`` (int): 配置可以生成中断的事件.可能的值有:

               - ``Pin.IRQ_FALLING``下降沿触发中断.
               - ``Pin.IRQ_RISING``上升沿触发中断.
               - ``Pin.IRQ_LOW_LEVEL``低电平触发中断.
               - ``Pin.IRQ_HIGH_LEVEL``高电平触发中断.

               这些值可以通过OR操作组合,以在多个事件上触发.

             - ``priority`` (int): 设置中断的优先级.它可以采取的值是特定于端口的,
               但更高的值总是代表更高的优先级.

             - ``wake`` (int | None): 选择此中断可以唤醒系统的电源模式.它可以是``machine.IDLE``、
               ``machine.SLEEP``或``machine.DEEPSLEEP``.这些值也可以通过OR操作组合,
               使引脚在多个电源模式下生成中断.

             - ``hard`` (bool): 如果为true,则使用硬件中断.这减少了引脚变化与处理程序被调用之间的延迟.
               硬中断处理程序可能不会分配内存;请参阅:ref:`isr_rules`.
               并非所有端口都支持此参数.

           返回:
            (Callable[..., Incomplete]): 回调对象.

        以下方法不是核心Pin API的一部分,仅在某些端口上实现.
        """
        ...

    def on(self) -> None:
        """
        将引脚设置为"1"输出电平.
        """
        ...

    def toggle(self) -> Incomplete:
        """
        将输出引脚从"0"切换到"1"或反之亦然.

        可用性: cc3200, esp32, esp8266, mimxrt, rp2, samd端口.
        """
        ...

    @overload
    def value(self) -> int:
        """
        此方法允许设置和获取引脚的值,取决于是否提供参数``x``.

        如果省略参数,则此方法获取引脚的数字逻辑电平,
        返回0或1,分别对应低电压和高电压信号.
        此方法的行为取决于引脚的模式:

          - ``Pin.IN`` - 该方法返回当前在引脚上存在的实际输入值.
          - ``Pin.OUT`` - 该方法的行为和返回值是未定义的.
          - ``Pin.OPEN_DRAIN`` - 如果引脚处于状态'0',则该方法的行为和
            返回值是未定义的.否则,如果引脚处于状态'1',该方法返回
            当前在引脚上存在的实际输入值.

        如果提供了参数,则此方法设置引脚的数字逻辑电平.
        参数``x``可以是任何能转换为布尔值的对象.
        如果它转换为``True``,则引脚设置为状态'1',否则设置为状态'0'.
        此方法的行为取决于引脚的模式:

          - ``Pin.IN`` - 该值存储在引脚的输出缓冲区中.引脚状态不变,
            它保持在高阻抗状态.一旦引脚模式更改为``Pin.OUT``或
            ``Pin.OPEN_DRAIN``,存储的值将在引脚上生效.
          - ``Pin.OUT`` - 输出缓冲区立即设置为给定值.
          - ``Pin.OPEN_DRAIN`` - 如果值为'0',则引脚设置为低电压状态.
            否则,引脚设置为高阻抗状态.

        返回:
            (int | None): 设置值时,此方法返回``None``.获取值时返回``int``.
        """

    @overload
    def value(self, x: Any, /) -> None:
        """
        此方法允许设置和获取引脚的值,取决于是否提供参数``x``.

        如果省略参数,则此方法获取引脚的数字逻辑电平,
        返回0或1,分别对应低电压和高电压信号.
        此方法的行为取决于引脚的模式:

          - ``Pin.IN`` - 该方法返回当前在引脚上存在的实际输入值.
          - ``Pin.OUT`` - 该方法的行为和返回值是未定义的.
          - ``Pin.OPEN_DRAIN`` - 如果引脚处于状态'0',则该方法的行为和
            返回值是未定义的.否则,如果引脚处于状态'1',该方法返回
            当前在引脚上存在的实际输入值.

        如果提供了参数,则此方法设置引脚的数字逻辑电平.
        参数``x``可以是任何能转换为布尔值的对象.
        如果它转换为``True``,则引脚设置为状态'1',否则设置为状态'0'.
        此方法的行为取决于引脚的模式:

          - ``Pin.IN`` - 该值存储在引脚的输出缓冲区中.引脚状态不变,
            它保持在高阻抗状态.一旦引脚模式更改为``Pin.OUT``或
            ``Pin.OPEN_DRAIN``,存储的值将在引脚上生效.
          - ``Pin.OUT`` - 输出缓冲区立即设置为给定值.
          - ``Pin.OPEN_DRAIN`` - 如果值为'0',则引脚设置为低电压状态.
            否则,引脚设置为高阻抗状态.

        返回:
            (None): 设置值时,此方法返回``None``.
        """

    def init(
        self,
        mode: int = -1,
        pull: int = -1,
        *,
        value: Any = None,
        drive: int | None = None,
        alt: int | None = None,
    ) -> None:
        """
        使用给定参数重新初始化引脚.只有指定的参数会被设置.引脚外设的其余状态将保持不变.
        有关参数的详细信息,请参阅构造函数文档.
        """
        ...

    class board:
        def __init__(self, *argv, **kwargs) -> None: ...

    def __init__(
        self,
        id: Any,
        /,
        mode: int = -1,
        pull: int = -1,
        *,
        value: Any = None,
        drive: int | None = None,
        alt: int | None = None,
    ) -> None:
        """
        访问与给定 ``id`` 关联的引脚外设(GPIO引脚).如果在构造函数中提供了额外的参数,
        则这些参数用于初始化引脚.未指定的任何设置将保持其先前的状态.

        参数如下:

          - ``id`` (Any): 是必需的,可以是任意对象.可能的值类型包括: int (内部Pin标识符)、
            str (Pin名称)和tuple (由[port, pin]组成的对).

          - ``mode`` (int): 指定引脚模式,可以是以下之一:

            - ``Pin.IN`` - 引脚配置为输入.如果作为输出查看,引脚处于高阻态.

            - ``Pin.OUT`` - 引脚配置为(正常)输出.

            - ``Pin.OPEN_DRAIN`` - 引脚配置为开漏输出.开漏输出的工作方式如下:
              如果输出值设置为0,则引脚在低电平下有效; 如果输出值为1,则引脚处于高阻态.
              并非所有端口都实现此模式,或者某些端口可能仅在特定引脚上实现.

            - ``Pin.ALT`` - 引脚配置为执行特定于端口的替代功能.对于以这种方式配置的引脚,
              任何其他Pin方法(除了 :meth:`Pin.init`)都不适用(调用它们将导致未定义的
              或特定于硬件的结果).并非所有端口都实现此模式.

            - ``Pin.ALT_OPEN_DRAIN`` - 与 ``Pin.ALT`` 相同,但引脚配置为开漏.
              并非所有端口都实现此模式.

            - ``Pin.ANALOG`` - 引脚配置为模拟输入,请参阅 :class:`ADC` 类.

          - ``pull`` (int): 指定引脚是否连接了(弱)上拉/下拉电阻,可以是以下之一:

            - ``None`` - 无上拉或下拉电阻.
            - ``Pin.PULL_UP`` - 启用上拉电阻.
            - ``Pin.PULL_DOWN`` - 启用下拉电阻.

          - ``value`` (Any): 仅对Pin.OUT和Pin.OPEN_DRAIN模式有效,如果给定,则指定初始输出引脚值,
            否则引脚外设的状态保持不变.

          - ``drive`` (int | None): 指定引脚的输出功率,可以是: ``Pin.LOW_POWER``、``Pin.MED_POWER``
            或 ``Pin.HIGH_POWER``.实际的电流驱动能力取决于端口.并非所有端口都实现此参数.

          - ``alt`` (int | None): 指定引脚的替代功能,其可取的值取决于端口.此参数仅对 ``Pin.ALT`` 和
            ``Pin.ALT_OPEN_DRAIN`` 模式有效.当引脚支持多个替代功能时,可以使用它.如果
            仅支持一个引脚替代功能,则不需要此参数.并非所有端口都实现此参数.

        如上所述,Pin类允许为特定引脚设置替代功能,但不指定对该引脚的任何进一步操作.
        配置为替代功能模式的引脚通常不用作GPIO,而是由其他硬件外设驱动.此类引脚支持的
        唯一操作是重新初始化,通过调用构造函数或 :meth:`Pin.init` 方法.如果配置为
        替代功能模式的引脚使用 ``Pin.IN``、``Pin.OUT`` 或 ``Pin.OPEN_DRAIN`` 重新初始化,
        则替代功能将从引脚中移除.
        """

    @overload
    def __call__(self) -> int:
        """
        Pin对象是可调用的.call方法提供了一个(快速)设置和获取引脚值的快捷方式.
        它等同于Pin.value([x]).有关更多详细信息,请参阅 :meth:`Pin.value`.
        """

    @overload
    def __call__(self, x: Any, /) -> None:
        """
        Pin对象是可调用的.call方法提供了一个(快速)设置和获取引脚值的快捷方式.
        它等同于Pin.value([x]).有关更多详细信息,请参阅 :meth:`Pin.value`.
        """

    @overload
    def mode(self) -> int:
        """
        获取或设置引脚模式.
        有关 ``mode`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200, stm32端口.
        """

    @overload
    def mode(self, mode: int, /) -> None:
        """
        获取或设置引脚模式.
        有关 ``mode`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200, stm32端口.
        """

    @overload
    def pull(self) -> int:
        """
        获取或设置引脚上拉/下拉状态.
        有关 ``pull`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200, stm32端口.
        """

    @overload
    def pull(self, pull: int, /) -> None:
        """
        获取或设置引脚上拉/下拉状态.
        有关 ``pull`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200, stm32端口.
        """

    @overload
    def drive(self, drive: int, /) -> None:
        """
        获取或设置引脚驱动强度.
        有关 ``drive`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200端口.
        """
        ...

    @overload
    def drive(self, /) -> int:
        """
        获取或设置引脚驱动强度.
        有关 ``drive`` 参数的详细信息,请参阅构造函数文档.

        可用性: cc3200端口.
        """

class TouchPad:
    def config(self, *args, **kwargs) -> Incomplete: ...
    def read(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, *argv, **kwargs) -> None: ...

class WDT:
    """
    WDT用于在应用程序崩溃并进入不可恢复状态时重启系统.一旦启动,它不能以任何方式
    停止或重新配置.启用后,应用程序必须定期"喂养"看门狗,以防止其过期并重置系统.

    使用示例::

        from machine import WDT
        wdt = WDT(timeout=2000)  # 启用它,超时为2秒.
        wdt.feed()

    此类的可用性: pyboard, WiPy, esp8266, esp32.
    """

    def feed(self) -> None:
        """
        喂养WDT以防止其重置系统.应用程序应该在合理的位置放置此调用,
        确保只有在验证一切正常运行后才喂养WDT.
        """
        ...

    def __init__(self, *, id: int = 0, timeout: int = 5000) -> None:
        """
        创建WDT对象并启动它.超时必须以毫秒为单位给出.
        一旦运行,超时就不能更改,WDT也不能停止.

        注意: 在esp32上,最小超时为1秒.在esp8266上,不能指定超时,
        它由底层系统决定.
        """

class SDCard:
    """
    ESP32的SD卡驱动
    
    此类提供对ESP32设备上SD卡功能的访问
    支持SDMMC和SPI两种接口
    """
    
    def __init__(
        self, 
        *,
        width: int = 1,
        cd: int = -1,
        wp: int = -1,
        slot: int = 1,
        cmd: int = -1,
        clk: int = -1,
        data_pins: Optional[Tuple[int, ...]] = None,
        spi_bus: Optional[SPI.Bus] = None,
        cs: int = -1,
        freq: int = 20000000
    ) -> None:
        """
        初始化SD卡
        
        参数:
            width (int): 总线宽度(1, 4或8位), 默认为1
            cd (int): 卡检测引脚, 默认为-1(不使用)
            wp (int): 写保护引脚, 默认为-1(不使用)
            slot (int): SD/MMC槽号(0-3), 默认为1
                  0,1为SD/MMC模式(如果支持)
                  2,3为SPI模式(如果支持)
            cmd (int): SDMMC模式的命令引脚, 默认为-1(使用默认引脚)
            clk (int): SDMMC模式的时钟引脚, 默认为-1(使用默认引脚)
            data_pins (Tuple[int, ...]): SDMMC模式的数据引脚, 数量必须与width匹配
            spi_bus (SPI): SPI模式的总线对象, 默认为None
            cs (int): SPI模式的片选引脚, 默认为-1
            freq (int): 时钟频率(Hz), 默认为20MHz
        """
        ...
    
    def deinit(self) -> None:
        """
        释放SD卡资源
        """
        ...
    
    def info(self) -> Tuple[int, int]:
        """
        获取SD卡信息
        
        返回:
            (Tuple[int, int]): 包含(容量, 块大小)的元组
                - 容量: SD卡总容量(字节)
                - 块大小: 块大小(字节)
        """
        ...
    
    def readblocks(self, block_num: int, buf: bytearray) -> bool:
        """
        从SD卡读取数据块
        
        参数:
            block_num (int): 起始块编号
            buf (bytearray): 存储读取数据的缓冲区
            
        返回:
            (bool): 成功返回True, 失败返回False
        """
        ...
    
    def writeblocks(self, block_num: int, buf: bytearray) -> bool:
        """
        向SD卡写入数据块
        
        参数:
            block_num (int): 起始块编号
            buf (bytearray): 包含要写入数据的缓冲区
            
        返回:
            (bool): 成功返回True, 失败返回False
        """
        ...
    
    def ioctl(self, cmd: int, arg: Any) -> int:
        """
        控制SD卡
        
        参数:
            cmd (int): 命令代码
            arg (Any): 命令参数
            
        返回:
            (int): 命令特定的返回值
        """
        ... 

        
class RTC:
    """
    RTC是一个独立的实时时钟 用于跟踪日期和时间

    使用示例:
        rtc = machine.RTC()
        rtc.datetime((2020, 1, 21, 2, 10, 32, 36, 0))
        print(rtc.datetime())

    RTC的文档状态较差 建议进行实验并使用 `dir` 方法查看可用属性
    """

    ALARM0: Incomplete

    @overload
    def init(self) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int, int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int, int, int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    @overload
    def init(self, datetime: tuple[int, int, int, int, int, int, int, int], /) -> None:
        """
        初始化RTC

        日期时间是以下形式的元组:
        (year, month, day, hour, minute, second, microsecond, tzinfo)

        必须提供所有八个参数. microsecond 和 tzinfo 值当前被忽略, 但将来可能会使用

        可用性: CC3200, ESP32, MIMXRT, SAMD. stm32和renesas-ra端口上的rtc.init()方法只是重新启动RTC, 不接受参数
        """

    def memory(self, data: Any | None = None) -> bytes:
        """
        将数据写入RTC内存

        参数:
            data (Any | None): 任何支持缓冲协议的对象 bytes bytearray memoryview array.array

        返回:
            (bytes): 写入的数据
        """
        ...

    def datetime(self, datetimetuple: Any | None = None) -> Tuple:
        """
        获取或设置RTC的日期和时间.

        不带参数时,此方法返回一个包含当前日期和时间的8元组.
        带1个参数(一个8元组)时,它设置日期和时间.

        8元组具有以下格式:

            (year, month, day, weekday, hours, minutes, seconds, subseconds)

        ``subseconds`` 字段的含义取决于硬件.
        """
        ...

    @overload
    def __init__(self, id: int = 0):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(self, id: int = 0, /, *, datetime: tuple[int, int, int]):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int]): 日期时间元组 (年 月 日)

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(self, id: int = 0, /, *, datetime: tuple[int, int, int, int]):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int, int]): 日期时间元组 (年 月 日 星期)

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(self, id: int = 0, /, *, datetime: tuple[int, int, int, int, int]):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时)

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(
        self, id: int = 0, /, *, datetime: tuple[int, int, int, int, int, int]
    ):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟)

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(
        self, id: int = 0, /, *, datetime: tuple[int, int, int, int, int, int, int]
    ):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟 秒)

        有关初始化参数 请参阅init方法
        """

    @overload
    def __init__(
        self, id: int = 0, /, *, datetime: tuple[int, int, int, int, int, int, int, int]
    ):
        """
        创建RTC对象

        参数:
            id (int): RTC实例ID 默认为0
            datetime (tuple[int, int, int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟 秒 微秒)

        有关初始化参数 请参阅init方法
        """

    @overload
    def value(self) -> int:
        """
        此方法允许设置和获取信号的值,取决于是否提供参数 ``x``.

        如果省略参数,则此方法获取信号电平,1表示信号被断言(激活),0表示信号未激活.

        如果提供参数,则此方法设置信号电平.参数 ``x`` 可以是任何能转换为布尔值的对象.
        如果它转换为 ``True``,则信号被激活,否则未激活.

        信号激活状态与底层引脚上实际逻辑电平之间的对应关系取决于信号是否反相(低电平有效).
        对于非反相信号,激活状态对应逻辑1,未激活状态对应逻辑0.对于反相/低电平有效信号,
        激活状态对应逻辑0,而未激活状态对应逻辑1.
        """

    @overload
    def value(self, x: Any, /) -> None:
        """
        此方法允许设置和获取信号的值,取决于是否提供参数 ``x``.

        如果省略参数,则此方法获取信号电平,1表示信号被断言(激活),0表示信号未激活.

        如果提供参数,则此方法设置信号电平.参数 ``x`` 可以是任何能转换为布尔值的对象.
        如果它转换为 ``True``,则信号被激活,否则未激活.

        信号激活状态与底层引脚上实际逻辑电平之间的对应关系取决于信号是否反相(低电平有效).
        对于非反相信号,激活状态对应逻辑1,未激活状态对应逻辑0.对于反相/低电平有效信号,
        激活状态对应逻辑0,而未激活状态对应逻辑1.
        """

    @overload
    def __init__(self, pin_obj: PinLike, invert: bool = False, /):
        """
        创建一个Signal对象.有两种创建方式:

        * 通过包装现有的Pin对象 - 适用于任何开发板的通用方法.
        * 通过直接将所需的Pin参数传递给Signal构造函数,
          跳过创建中间Pin对象的需要.在许多(但不是所有)开发板上可用.

        参数如下:

          - ``pin_obj`` (PinLike): 是现有的Pin对象.

          - ``pin_arguments`` (Any): 与可传递给Pin构造函数的参数相同.

          - ``invert`` (bool): 如果为True,信号将被反相(低电平有效).
        """

    @overload
    def __init__(
        self,
        id: PinLike,
        /,
        mode: int = -1,
        pull: int = -1,
        *,
        value: Any = None,
        drive: int | None = None,
        alt: int | None = None,
        invert: bool = False,
    ):
        """
        创建一个Signal对象.有两种创建方式:

        * 通过包装现有的Pin对象 - 适用于任何开发板的通用方法.
        * 通过直接将所需的Pin参数传递给Signal构造函数,
          跳过创建中间Pin对象的需要.在许多(但不是所有)开发板上可用.

        参数如下:

          - ``pin_obj`` (PinLike): 是现有的Pin对象.

          - ``pin_arguments`` (Any): 与可传递给Pin构造函数的参数相同.

          - ``invert`` (bool): 如果为True,信号将被反相(低电平有效).
        """

    @overload
    def alarm(self, id: int, time: int, /, *, repeat: bool = False) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (int): 毫秒值 用于将闹钟设置为当前时间 + time_in_ms
            repeat (bool): 是否周期性重复 默认为False

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(self, id: int, time: tuple[int, int, int], /) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int]): 日期时间元组 (年 月 日)

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(self, id: int, time: tuple[int, int, int, int], /) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int, int]): 日期时间元组 (年 月 日 星期)

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(self, id: int, time: tuple[int, int, int, int, int], /) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时)

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(self, id: int, time: tuple[int, int, int, int, int, int], /) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟)

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(self, id: int, time: tuple[int, int, int, int, int, int, int], /) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟 秒)

        返回:
            (None): 无返回值
        """

    @overload
    def alarm(
        self, id: int, time: tuple[int, int, int, int, int, int, int, int], /
    ) -> None:
        """
        设置RTC闹钟

        参数:
            id (int): 闹钟ID
            time (tuple[int, int, int, int, int, int, int, int]): 日期时间元组 (年 月 日 星期 小时 分钟 秒 微秒)

        返回:
            (None): 无返回值
        """

class SoftI2C(I2C):
    """
    构造一个新的软件I2C对象

    参数:
        scl (PinLike): SCL线的引脚对象
        sda (PinLike): SDA线的引脚对象
        freq (int): SCL的最大频率 默认为400000Hz
        timeout (int): 等待时钟延展的最大时间 微秒 默认为50000微秒
    """

    def readfrom_mem_into(self, *args, **kwargs) -> Incomplete: ...
    def readfrom_into(self, *args, **kwargs) -> Incomplete: ...
    def readfrom_mem(self, *args, **kwargs) -> Incomplete: ...
    def writeto_mem(self, *args, **kwargs) -> Incomplete: ...
    def scan(self, *args, **kwargs) -> Incomplete: ...
    def writeto(self, *args, **kwargs) -> Incomplete: ...
    def writevto(self, *args, **kwargs) -> Incomplete: ...
    def start(self, *args, **kwargs) -> Incomplete: ...
    def readfrom(self, *args, **kwargs) -> Incomplete: ...
    def readinto(self, *args, **kwargs) -> Incomplete: ...
    def init(self, *args, **kwargs) -> Incomplete: ...
    def stop(self, *args, **kwargs) -> Incomplete: ...
    def write(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, scl, sda, *, freq=400000, timeout=50000) -> None: ...

class SPI:
    """
    SPI是由控制器驱动的同步串行协议

    它由3条线组成: SCK MOSI MISO
    多个设备可以共享同一条总线
    每个设备应该有一个单独的第4个信号CS 片选 用于选择总线上进行通信的特定设备
    CS信号的管理应该在用户代码中进行 通过machine.Pin类

    硬件和软件SPI实现都通过 `machine.SPI` 和 `machine.SoftSPI` 类提供
    硬件SPI使用系统的底层硬件支持来执行读/写操作, 通常高效快速, 但可能对可用的引脚有限制
    软件SPI通过位操作实现, 可以在任何引脚上使用, 但效率不如硬件SPI高
    这些类具有相同的可用方法, 主要区别在于它们的构造方式

    使用示例:
        from machine import SPI, Pin

        spi = SPI(0, baudrate=400000)           # 创建频率为400kHz的SPI外设0
                                                # 根据用例, 可能需要额外参数
                                                # 来选择总线特性和/或要使用的引脚
        cs = Pin(4, mode=Pin.OUT, value=1)      # 在引脚4上创建片选

        try:
            cs(0)                               # 选择外设
            spi.write(b"12345678")              # 写入8个字节, 不关心接收到的数据
        finally:
            cs(1)                               # 取消选择外设

        try:
            cs(0)                               # 选择外设
            rxdata = spi.read(8, 0x42)          # 读取8个字节, 同时为每个字节写入0x42
        finally:
            cs(1)                               # 取消选择外设

        rxdata = bytearray(8)
        try:
            cs(0)                               # 选择外设
            spi.readinto(rxdata, 0x42)          # 原地读取8个字节, 同时为每个字节写入0x42
        finally:
            cs(1)                               # 取消选择外设

        txdata = b"12345678"
        rxdata = bytearray(len(txdata))
        try:
            cs(0)                               # 选择外设
            spi.write_readinto(txdata, rxdata)  # 同时写入和读取字节
        finally:
            cs(1)                               # 取消选择外设
    """

    LSB: Final[int] = 1
    MSB: Final[int] = 0
    CONTROLLER: Incomplete

    class Bus:
        """
        SPI总线类, 用于创建SPI总线
        """

        def __init__(self, *, host: int, mosi: int, miso: int, sck: int):
            """
            在给定总线上构造SPI.Bus对象

            参数:
                host (int): SPI主机编号
                mosi (int): MOSI引脚编号
                miso (int): MISO引脚编号
                sck (int): SCK引脚编号
            """
            ...

        def deinit(self) -> None:
            """
            关闭SPI总线
            """
            ...

    class DualBus:
        """
        SPI双线总线类, 用于创建双线SPI总线
        """

        def __init__(self, *, host: int, data0: int, data1: int, sck: int):
            """
            在给定总线上构造SPI.DualBus对象

            参数:
                host (int): SPI主机编号
                data0 (int): 数据0引脚编号
                data1 (int): 数据1引脚编号
                sck (int): SCK引脚编号
            """
            ...

        def deinit(self) -> None:
            """
            关闭SPI总线
            """
            ...

    class QuadBus:
        """
        SPI四线总线类, 用于创建四线SPI总线
        """

        def __init__(
            self, *, host: int, data0: int, data1: int, data2: int, data3: int, sck: int
        ):
            """
            在给定总线上构造SPI.QuadBus对象

            参数:
                host (int): SPI主机编号
                data0 (int): 数据0引脚编号
                data1 (int): 数据1引脚编号
                data2 (int): 数据2引脚编号
                data3 (int): 数据3引脚编号
                sck (int): SCK引脚编号
            """
            ...

        def deinit(self) -> None:
            """
            关闭SPI总线
            """
            ...

    class OctalBus:
        """
        SPI八线总线类, 用于创建八线SPI总线
        """

        def __init__(
            self,
            *,
            host: int,
            data0: int,
            data1: int,
            data2: int,
            data3: int,
            data4: int,
            data5: int,
            data6: int,
            data7: int,
            sck: int,
        ):
            """
            在给定总线上构造SPI.OctalBus对象

            参数:
                host (int): SPI主机编号
                data0 (int): 数据0引脚编号
                data1 (int): 数据1引脚编号
                data2 (int): 数据2引脚编号
                data3 (int): 数据3引脚编号
                data4 (int): 数据4引脚编号
                data5 (int): 数据5引脚编号
                data6 (int): 数据6引脚编号
                data7 (int): 数据7引脚编号
                sck (int): SCK引脚编号
            """
            ...

        def deinit(self) -> None:
            """
            关闭SPI总线
            """
            ...

    class Device:
        """
        SPI设备类, 用于创建SPI设备
        """

        def __init__(
            self,
            *,
            spi_bus: Union[
                "SPI.Bus",
                "SPI.DualBus",
                "SPI.QuadBus",
                "SPI.OctalBus",
            ],
            freq: int,
            cs: int,
            polarity: int = 0,
            phase: int = 0,
            bits: int = 8,
            firstbit: int = 0,  # 默认使用MSB
            dual: bool = False,
            quad: bool = False,
            octal: bool = False,
        ):
            """
            构造SPI.Device对象

            参数:
                spi_bus (SPI.Bus | SPI.DualBus | SPI.QuadBus | SPI.OctalBus): SPI总线对象
                freq (int): 设备通信频率
                cs (int): 片选引脚编号
                polarity (int): 空闲时钟线所处的电平 0或1
                phase (int): 在第一个或第二个时钟边沿采样数据 0或1
                bits (int): 每次传输的位宽
                firstbit (int): MSB(0)或LSB(1)
                dual (bool): 是否使用双线模式
                quad (bool): 是否使用四线模式
                octal (bool): 是否使用八线模式
            """
            ...

        def deinit(self) -> None:
            """
            关闭SPI设备
            """
            ...

        def read(self, nbytes: int, write: int = 0x00, /) -> bytes:
            """
            读取指定字节数 同时连续写入单个字节

            参数:
                nbytes (int): 要读取的字节数
                write (int): 每次读取时要写入的单个字节 默认为0x00

            返回:
                (bytes): 包含所读取数据的bytes对象
            """
            ...

        def readinto(self, buf: AnyWritableBuf, write: int = 0x00, /) -> int | None:
            """
            读取数据到指定缓冲区中 同时连续写入单个字节

            参数:
                buf (AnyWritableBuf): 用于接收读取数据的缓冲区
                write (int): 每次读取时要写入的单个字节 默认为0x00

            返回:
                (int | None): 读取的字节数或None
            """
            ...

        def write(self, buf: AnyReadableBuf, /) -> int | None:
            """
            写入缓冲区中的字节

            参数:
                buf (AnyReadableBuf): 包含要写入字节的缓冲区

            返回:
                (int | None): 写入的字节数或None
            """
            ...

        def write_readinto(
            self, write_buf: AnyReadableBuf, read_buf: AnyWritableBuf, /
        ) -> int | None:
            """
            从write_buf写入字节 同时读取到read_buf中

            参数:
                write_buf (AnyReadableBuf): 包含要写入数据的缓冲区
                read_buf (AnyWritableBuf): 用于接收读取数据的缓冲区

            返回:
                (int | None): 写入的字节数或None
            """
            ...

    def deinit(self) -> None:
        """
        关闭SPI总线
        """
        ...
    ...

class Signal:
    """
    控制一个数字信号 例如通过 `Pin` 对象

    可以像创建 `Pin` 对象一样传递 `Pin` 对象或引脚号
    一个 `Signal` 对象可以像函数一样被调用以快速获取或设置它所表示的信号值
    """

    def off(self) -> None:
        """
        将信号设置为其非活动状态

        如果 `value` 为0 则设置为0 否则设置为1
        """
        ...

    @overload
    def value(self) -> int:
        """
        获取或设置信号的当前数字值

        不带参数时 返回信号的值 0或1
        带参数时 设置信号的值
        """

    @overload
    def value(self, x: Any, /) -> None:
        """
        获取或设置信号的当前数字值

        不带参数时 返回信号的值 0或1
        带参数时 设置信号的值
        """

    def on(self) -> None:
        """
        将信号设置为其活动状态

        如果 `value` 为1 则设置为1 否则设置为0
        """
        ...

    def __init__(self, pin: PinLike, /, *, value: bool = False, invert: bool = False):
        """
        构造并返回一个新的 `Signal` 对象

        参数:
            pin (PinLike): 引脚对象或整数引脚号
            value (bool): 信号的初始值 False表示非活动状态 默认为False
            invert (bool): 是否反转信号的逻辑 默认为False
        """

    @overload
    def __call__(self) -> int:
        """
        Signal对象是可调用的 调用方法提供了一个 快速 设置和获取信号值的快捷方式

        它等同于 `Signal.value([x])`
        """

    @overload
    def __call__(self, x: Any, /) -> None:
        """
        Signal对象是可调用的 调用方法提供了一个 快速 设置和获取信号值的快捷方式

        它等同于 `Signal.value([x])`
        """