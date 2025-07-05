"""
数学函数模块

该 `math` 模块提供了一些基本的数学函数 用于处理浮点数

注意: 在pyboard上 浮点数具有32位精度

可用性: 不适用于WiPy 需要浮点支持此模块
"""

# MCU: {'variant': 'SPIRAM', 'build': '', 'arch': 'xtensawin', 'port': 'esp32', 'board': 'ESP32_GENERIC', 'board_id': 'ESP32_GENERIC-SPIRAM', 'mpy': 'v6.3', 'ver': '1.25.0', 'family': 'micropython', 'cpu': 'ESP32', 'version': '1.25.0'}
# Stubber: v1.25.0
from __future__ import annotations
from _typeshed import Incomplete
from typing import SupportsFloat, Tuple
from typing_extensions import Awaitable, TypeAlias, TypeVar

inf: float = inf
nan: float = nan
pi: float = 3.141593
e: float = 2.718282
tau: float = 6.283185

def ldexp(x: SupportsFloat, exp: int, /) -> float:
    """
    计算 x 乘以 2 的 exp 次幂

    参数:
        x (SupportsFloat): 基数
        exp (int): 指数

    返回:
        (float): 计算结果 x * (2**exp)
    """
    ...

def lgamma(x: SupportsFloat, /) -> float:
    """
    计算伽马函数的自然对数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): 伽马函数 x 的自然对数
    """
    ...

def trunc(x: SupportsFloat, /) -> int:
    """
    返回截断后的整数

    参数:
        x (SupportsFloat): 输入浮点数

    返回:
        (int): 朝0方向取整后的整数
    """
    ...

def isclose(*args, **kwargs) -> Incomplete: ...
def gamma(x: SupportsFloat, /) -> float:
    """
    计算伽马函数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): 伽马函数 x 的结果
    """
    ...

def isnan(x: SupportsFloat, /) -> bool:
    """
    检查是否为非数字

    参数:
        x (SupportsFloat): 输入值

    返回:
        (bool): 如果x是非数字 则返回True
    """
    ...

def isfinite(x: SupportsFloat, /) -> bool:
    """
    检查是否为有限数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (bool): 如果x是有限数 则返回True
    """
    ...

def isinf(x: SupportsFloat, /) -> bool:
    """
    检查是否为无限数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (bool): 如果x是无限数 则返回True
    """
    ...

def sqrt(x: SupportsFloat, /) -> float:
    """
    计算平方根

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的平方根
    """
    ...

def sinh(x: SupportsFloat, /) -> float:
    """
    计算双曲正弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的双曲正弦
    """
    ...

def log(x: SupportsFloat, /) -> float:
    """
    计算对数

    参数:
        x (SupportsFloat): 真数

    返回:
        (float): x的自然对数
    """
    ...

def tan(x: SupportsFloat, /) -> float:
    """
    计算正切

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的正切
    """
    ...

def tanh(x: SupportsFloat, /) -> float:
    """
    计算双曲正切

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的双曲正切
    """
    ...

def log2(x: SupportsFloat, /) -> float:
    """
    计算以2为底的对数

    参数:
        x (SupportsFloat): 真数

    返回:
        (float): 以2为底的x的对数
    """
    ...

def log10(x: SupportsFloat, /) -> float:
    """
    计算以10为底的对数

    参数:
        x (SupportsFloat): 真数

    返回:
        (float): 以10为底的x的对数
    """
    ...

def sin(x: SupportsFloat, /) -> float:
    """
    计算正弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的正弦
    """
    ...

def modf(x: SupportsFloat, /) -> Tuple:
    """
    分解浮点数的整数和小数部分

    参数:
        x (SupportsFloat): 输入浮点数

    返回:
        (Tuple): 包含x的小数部分和整数部分的元组 两者与x同符号
    """
    ...

def radians(x: SupportsFloat, /) -> float:
    """
    将度数转换为弧度

    参数:
        x (SupportsFloat): 度数

    返回:
        (float): x转换为弧度后的值
    """
    ...

def atanh(x: SupportsFloat, /) -> float:
    """
    计算反双曲正切

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反双曲正切
    """
    ...

def atan2(y: SupportsFloat, x: SupportsFloat, /) -> float:
    """
    计算y/x的反正切主值

    参数:
        y (SupportsFloat): y坐标
        x (SupportsFloat): x坐标

    返回:
        (float): y/x的反正切主值
    """
    ...

def atan(x: SupportsFloat, /) -> float:
    """
    计算反正切

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反正切
    """
    ...

def ceil(x: SupportsFloat, /) -> int:
    """
    向上取整

    参数:
        x (SupportsFloat): 输入浮点数

    返回:
        (int): 朝正无穷方向取整后的整数
    """
    ...

def copysign(x: SupportsFloat, y: SupportsFloat, /) -> float:
    """
    返回带有y符号的x值

    参数:
        x (SupportsFloat): 数值
        y (SupportsFloat): 符号来源

    返回:
        (float): 带有y符号的x值
    """
    ...

def frexp(x: SupportsFloat, /) -> tuple[float, int]:
    """
    将浮点数分解为尾数和指数

    参数:
        x (SupportsFloat): 输入浮点数

    返回:
        (tuple[float, int]): 包含尾数m和指数e的元组 满足x = m * 2**e
    """
    ...

def acos(x: SupportsFloat, /) -> float:
    """
    计算反余弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反余弦
    """
    ...

def pow(x: SupportsFloat, y: SupportsFloat, /) -> float:
    """
    计算x的y次幂

    参数:
        x (SupportsFloat): 底数
        y (SupportsFloat): 指数

    返回:
        (float): x的y次幂的结果
    """
    ...

def asinh(x: SupportsFloat, /) -> float:
    """
    计算反双曲正弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反双曲正弦
    """
    ...

def acosh(x: SupportsFloat, /) -> float:
    """
    计算反双曲余弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反双曲余弦
    """
    ...

def asin(x: SupportsFloat, /) -> float:
    """
    计算反正弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的反正弦
    """
    ...

def factorial(*args, **kwargs) -> Incomplete: ...
def fabs(x: SupportsFloat, /) -> float:
    """
    计算绝对值

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的绝对值
    """
    ...

def expm1(x: SupportsFloat, /) -> float:
    """
    计算e的x次幂减1

    参数:
        x (SupportsFloat): 指数

    返回:
        (float): exp(x) - 1 的结果
    """
    ...

def floor(x: SupportsFloat, /) -> int:
    """
    向下取整

    参数:
        x (SupportsFloat): 输入浮点数

    返回:
        (int): 朝负无穷方向取整后的整数
    """
    ...

def fmod(x: SupportsFloat, y: SupportsFloat, /) -> float:
    """
    计算浮点余数

    参数:
        x (SupportsFloat): 被除数
        y (SupportsFloat): 除数

    返回:
        (float): x除以y的余数
    """
    ...

def cos(x: SupportsFloat, /) -> float:
    """
    计算余弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的余弦
    """
    ...

def degrees(x: SupportsFloat, /) -> float:
    """
    将弧度转换为度数

    参数:
        x (SupportsFloat): 弧度值

    返回:
        (float): x转换为度数后的值
    """
    ...

def cosh(x: SupportsFloat, /) -> float:
    """
    计算双曲余弦

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的双曲余弦
    """
    ...

def exp(x: SupportsFloat, /) -> float:
    """
    计算指数函数

    参数:
        x (SupportsFloat): 指数

    返回:
        (float): e的x次幂
    """
    ...

def erf(x: SupportsFloat, /) -> float:
    """
    计算误差函数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的误差函数值
    """
    ...

def erfc(x: SupportsFloat, /) -> float:
    """
    计算补余误差函数

    参数:
        x (SupportsFloat): 输入值

    返回:
        (float): x的补余误差函数值
    """
    ...
