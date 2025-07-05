"""
时间相关函数.

MicroPython模块: https://docs.micropython.org/en/v1.25.0/library/time.html

CPython模块: :mod:`python:time` https://docs.python.org/3/library/time.html .

``time``模块提供了获取当前时间和日期、测量时间间隔以及实现延时的函数.

**时间纪元**: Unix端口使用POSIX系统标准的1970-01-01 00:00:00 UTC作为纪元起点.
然而,一些嵌入式端口使用2000-01-01 00:00:00 UTC作为纪元起点.
纪元年份可通过``gmtime(0)[0]``确定.

**维护实际日历日期/时间**: 这需要一个实时时钟(RTC).在具有底层操作系统(包括某些RTOS)的系统上,
RTC可能是隐式的.设置和维护实际日历时间是操作系统/RTOS的责任,在MicroPython之外完成,
MicroPython只使用操作系统API来查询日期/时间.然而在裸机端口上,系统时间依赖于
``machine.RTC()``对象.当前日历时间可以使用``machine.RTC().datetime(tuple)``函数设置,
并通过以下方式维护:

* 使用备用电池(可能是特定板的附加可选组件).
* 使用网络时间协议(需要由端口/用户设置).
* 用户在每次上电时手动设置(许多板然后在硬复位之间保持RTC时间,尽管有些可能需要在这种情况下再次设置).

如果使用系统/MicroPython RTC没有维护实际日历时间,
则需要参考当前绝对时间的下面函数可能无法按预期工作.

---
模块: 'time' on micropython-v1.25.0-esp32-ESP32_GENERIC-SPIRAM
"""

# MCU: {'variant': 'SPIRAM', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC-SPIRAM', 'mpy': 'v6.3', 'ver': '1.25.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.25.0'}
# Stubber: v1.25.0
from __future__ import annotations
from _typeshed import Incomplete
from _mpy_shed import _TimeTuple
from typing import Tuple
from typing_extensions import Awaitable, TypeAlias, TypeVar

_TicksMs: TypeAlias = int
_TicksUs: TypeAlias = int
_TicksCPU: TypeAlias = int
_Ticks = TypeVar("_Ticks", _TicksMs, _TicksUs, _TicksCPU, int)

def ticks_diff(ticks1: _Ticks, ticks2: _Ticks, /) -> int:
    """
    测量`ticks_ms()`, `ticks_us()`或`ticks_cpu()`函数返回的值之间的时钟周期差,
    作为一个可能会环绕的有符号值.
    
    参数顺序与减法运算符相同,`ticks_diff(ticks1, ticks2)`与`ticks1 - ticks2`含义相同.
    然而,`ticks_ms()`等函数返回的值可能会环绕,所以直接对它们进行减法会产生错误结果.
    这就是为什么需要`ticks_diff()`,它实现了模运算(更具体地说,环形)算术,
    即使是环绕值也能产生正确结果(只要它们之间不太远,见下文).
    
    函数返回范围为[*-TICKS_PERIOD/2* .. *TICKS_PERIOD/2-1*]的**有符号**值
    (这是二进制补码有符号整数的典型范围定义).如果结果为负,表示*ticks1*发生在*ticks2*之前.
    否则,表示*ticks1*发生在*ticks2*之后.这**仅**在*ticks1*和*ticks2*相隔不超过
    *TICKS_PERIOD/2-1*个时钟周期时成立.如果不满足该条件,将返回错误结果.
    
    参数:
        ticks1: (_Ticks) 第一个时钟计数值
        ticks2: (_Ticks) 第二个时钟计数值
        
    返回:
        int: 两个时钟计数值之间的差值
    """
    ...

def ticks_add(ticks: _Ticks, delta: int, /) -> _Ticks:
    """
    将时钟计数值偏移给定的数量,可以是正数也可以是负数.
    
    给定一个*ticks*值,此函数允许计算其前或后*delta*个时钟周期的值,
    遵循时钟值的模运算定义(参见上面的`ticks_ms()`).
    *ticks*参数必须是直接调用`ticks_ms()`, `ticks_us()`或`ticks_cpu()`函数的结果
    (或之前调用`ticks_add()`的结果).然而,*delta*可以是任意整数或数值表达式.
    
    `ticks_add()`对于计算事件/任务的截止时间很有用.
    (注意:你必须使用`ticks_diff()`函数来处理截止时间.)
    
    参数:
        ticks: (_Ticks) 原始时钟计数值
        delta: int 要添加的偏移量(正或负)
        
    返回:
        _Ticks: 计算后的新时钟计数值
    """
    ...

def ticks_cpu() -> _TicksCPU:
    """
    类似于`ticks_ms()`和`ticks_us()`,但具有系统中可能的最高分辨率.
    
    这通常是CPU时钟,这就是为什么该函数被这样命名.但它不必是CPU时钟,
    系统中可用的其他计时源(例如高分辨率定时器)也可以使用.
    此函数的确切计时单位(分辨率)在``time``模块级别上没有指定,
    但特定端口的文档可能会提供更具体的信息.
    
    此函数适用于非常精细的基准测试或非常紧凑的实时循环.避免在可移植代码中使用它.
    
    可用性: 并非每个端口都实现此函数.
    
    返回:
        _TicksCPU: CPU时钟计数器值
    """
    ...

def time() -> int:
    """
    返回自纪元以来的秒数(整数),假设底层RTC已按上述方式设置和维护.
    
    如果未设置RTC,此函数返回自特定端口参考时间点以来的秒数
    (对于没有电池供电RTC的嵌入式板,通常是自上电或复位以来).
    如果要开发可移植的MicroPython应用程序,不应依赖此函数提供高于秒的精度.
    
    如果需要更高精度的绝对时间戳,请使用`time_ns()`.
    如果相对时间可接受,则使用`ticks_ms()`和`ticks_us()`函数.
    如果需要日历时间,不带参数的`gmtime()`或`localtime()`是更好的选择.
    
    提示:与CPython的差异
       :class: attention
       
       在CPython中,此函数返回自Unix纪元(1970-01-01 00:00 UTC)以来的秒数,
       作为浮点数,通常具有微秒精度.在MicroPython中,只有Unix端口使用相同的纪元,
       如果浮点精度允许,则返回亚秒精度.嵌入式硬件通常没有表示长时间范围和亚秒精度的
       浮点精度,因此它们使用具有秒精度的整数值.一些嵌入式硬件也缺乏电池供电的RTC,
       因此返回自上次通电或其他相对硬件特定点(例如复位)以来的秒数.
       
    返回:
        int: 自纪元以来的秒数
    """
    ...

def ticks_ms() -> int:
    """
    返回一个递增的毫秒计数器,具有任意参考点,在某个值后环绕.
    
    环绕值没有明确公开,但我们将其称为*TICKS_MAX*以简化讨论.
    值的周期是*TICKS_PERIOD = TICKS_MAX + 1*. *TICKS_PERIOD*保证是2的幂,
    但在不同端口间可能不同.相同的周期值用于所有`ticks_ms()`, `ticks_us()`, 
    `ticks_cpu()`函数(为了简单).
    
    因此,这些函数将返回范围[*0* .. *TICKS_MAX*]内的值,包括两端,共*TICKS_PERIOD*个值.
    注意,只使用非负值.在大多数情况下,应将这些函数返回的值视为不透明的.
    对它们可用的操作只有下面描述的`ticks_diff()`和`ticks_add()`函数.
    
    注意: 直接对这些值执行标准数学运算(+, -)或关系运算符(<, <=, >, >=)
    将导致无效结果.执行数学运算后将其结果作为参数传递给`ticks_diff()`或
    `ticks_add()`也会导致后者函数产生无效结果.
    
    返回:
        int: 毫秒计数器值
    """
    ...

def ticks_us() -> _TicksUs:
    """
    与上面的`ticks_ms()`类似,但以微秒为单位.
    
    返回:
        _TicksUs: 微秒计数器值
    """
    ...

def time_ns() -> int:
    """
    与`time()`类似,但返回自纪元以来的纳秒数,作为整数(通常是大整数,因此会在堆上分配).
    
    返回:
        int: 自纪元以来的纳秒数
    """
    ...

def localtime(secs: int | None = None, /) -> Tuple:
    """
    将以秒表示的时间*secs*(自纪元以来,见上文)转换为8元组,其中包含:
    ``(year, month, mday, hour, minute, second, weekday, yearday)``
    
    如果未提供*secs*或为None,则使用RTC的当前时间.
    
    `gmtime()`函数返回UTC中的日期时间元组,而`localtime()`返回本地时间的日期时间元组.
    
    8元组中各项的格式为:
    
    * year    包括世纪(例如2014)
    * month   是1-12
    * mday    是1-31
    * hour    是0-23
    * minute  是0-59
    * second  是0-59
    * weekday 是0-6表示周一至周日
    * yearday 是1-366
    
    参数:
        secs: (int|None) 自纪元以来的秒数,默认为None表示使用当前时间
        
    返回:
        Tuple: 包含日期和时间信息的8元组
    """
    ...

def sleep_us(us: int, /) -> None:
    """
    延时指定的微秒数,应为正数或0.
    
    此函数尝试提供至少*us*微秒的精确延时,但如果系统有其他更高优先级的处理需要执行,
    可能需要更长时间.
    
    参数:
        us: int 要延时的微秒数
    """
    ...

def gmtime(secs: int | None = None, /) -> Tuple:
    """
    将以秒表示的时间*secs*(自纪元以来,见上文)转换为8元组,其中包含:
    ``(year, month, mday, hour, minute, second, weekday, yearday)``
    
    如果未提供*secs*或为None,则使用RTC的当前时间.
    
    `gmtime()`函数返回UTC中的日期时间元组,而`localtime()`返回本地时间的日期时间元组.
    
    8元组中各项的格式为:
    
    * year    包括世纪(例如2014)
    * month   是1-12
    * mday    是1-31
    * hour    是0-23
    * minute  是0-59
    * second  是0-59
    * weekday 是0-6表示周一至周日
    * yearday 是1-366
    
    参数:
        secs: (int|None) 自纪元以来的秒数,默认为None表示使用当前时间
        
    返回:
        Tuple: 包含日期和时间信息的8元组
    """
    ...

def sleep_ms(ms: int, /) -> None:
    """
    延时指定的毫秒数,应为正数或0.
    
    此函数将至少延时给定的毫秒数,但如果需要执行其他处理,如中断处理程序或其他线程,
    可能需要更长时间.传入0作为*ms*仍将允许执行这些其他处理.
    使用`sleep_us()`可获得更精确的延时.
    
    参数:
        ms: int 要延时的毫秒数
    """
    ...

def mktime(local_time: _TimeTuple, /) -> int:
    """
    这是localtime的反函数.它的参数是一个完整的8元组,按照localtime表示时间.
    它返回一个整数,表示自2000年1月1日以来的秒数.
    
    参数:
        local_time: (_TimeTuple) 表示日期和时间的8元组
        
    返回:
        int: 自2000年1月1日以来的秒数
    """
    ...

def sleep(seconds: float, /) -> None:
    """
    休眠给定的秒数.某些板可能接受*seconds*作为浮点数,以休眠小数秒.
    
    注意,其他板可能不接受浮点参数,为了兼容它们,请使用`sleep_ms()`和`sleep_us()`函数.
    
    参数:
        seconds: float 要休眠的秒数
    """
    ...
