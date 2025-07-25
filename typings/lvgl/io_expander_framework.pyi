from typing import Union, ClassVar, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import machine
    import i2c

class Pin(object):
    IN = 0x00
    OUT = 0x01
    OPEN_DRAIN = 0x02

    IRQ_RISING = 0x01
    IRQ_FALLING = 0x02

    PULL_UP = 0x01
    PULL_DOWN = 0x02

    _id: int = ...
    _mode: int = ...
    _buf: bytearray = ...
    _mv: memoryview = ...
    _adc: Union["ADC", None] = ...
    _pwm: Union["PWM", None] = ...
    _irq: Union[Callable[["Pin"], None], None] = ...
    _int_pin: ClassVar[machine.Pin | None] = ...
    _reg_int_pins: ClassVar[list["Pin"]] = ...
    _device: ClassVar[i2c.I2C.Device | machine.SPI.Device | None] = ...
    _irq_input_state: int = 0

    def __init__(self, id: int, mode: int = -1, pull: int | None = -1, value: int | float = -1):
        """
        初始化引脚
        
        参数:
            id (int): 引脚ID
            mode (int): 引脚模式,默认-1
            pull (int | None): 上拉下拉,默认-1
            value (int | float): 初始值,默认-1
        返回:
            (None): 无返回值
        """
        ...

    @classmethod
    def _int_cb(cls, pin: machine.Pin) -> None:
        ...

    def _interrupt_cb(self) -> None:
        ...

    @classmethod
    def set_int_pin(cls, pin_num: int, pull: int = -1):
        ...

    @classmethod
    def set_device(cls, device: i2c.I2C.Device | machine.SPI.Device):
        ...


    def init(self, mode: int = -1, pull: int | None = -1, value: int = -1) -> None:
        ...

    def value(self, x: int | float = -1) -> int | float | None:
        ...

    def __call__(self, x: int | float = -1) -> int | float | None:
        ...

    def on(self) -> None:
        ...

    def off(self) -> None:
        ...

    def low(self) -> None:
        ...

    def high(self) -> None:
        ...

    def mode(self, mode: int = -1) -> int | None:
        ...

    def irq(self, handler: Union[Callable[["Pin"], None], None], trigger: int = IRQ_RISING | IRQ_FALLING) -> None:
        ...

    def _set_irq(self, handler: Union[Callable[["Pin"], None], None], trigger: int) -> None:
        ...

    def _set_pull(self, pull: int | None) -> None:
        ...

    def _set_dir(self, direction: int) -> None:
        ...

    def _set_level(self, level: int | float) -> None:
        ...

    def _get_level(self) -> int | float | None:
        ...


class PWM:
    _pin: Pin = ...

    def __init__(self, pin: Pin, freq: int = -1, duty: int = -1):
        ...

    def init(self, freq: int = -1, duty: int = -1) -> None:
        ...

    def deinit(self) -> None:
        ...

    def freq(self, freq: int = -1) -> int | None:
        ...

    def duty(self, duty: int = -1) -> int | None:
        ...


class ADC:
    WIDTH_9BIT = 0
    WIDTH_10BIT = 1
    WIDTH_11BIT = 2
    WIDTH_12BIT = 3
    WIDTH_13BIT = 4

    ATTN_0DB = 0
    ATTN_2_5DB = 1
    ATTN_6DB = 2
    ATTN_11DB = 3

    _pin: Pin = ...
    _attn: int = ...
    _width: int = ...

    _min_read: ClassVar[int] = ...
    _max_read: ClassVar[int] = ...


    def __init__(self, pin: Pin, atten: int = -1):
        ...

    def init(self, atten: int = -1) -> None:
        ...

    def deinit(self) -> None:
        ...

    def read_uv(self) -> float:
        ...

    def atten(self, atten: int = -1) -> None:
        ...

    def width(self, width: int) -> None:
        ...

    def read(self) -> int:
        ...

    def _read(self) -> int:
        ...

    def _init(self, atten) -> None:
        ...
