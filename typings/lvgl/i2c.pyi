# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from typing import Optional, Union
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import array


_BUFFER_TYPE = Union[bytearray, bytes, memoryview, array.array]


class I2C(object):
    class Bus(object):

        def __init__(
            self,
            host: Union[str, int],
            scl: Union[str, int],
            sda: Union[str, int],
            freq: int = 4000000,
            use_locks: bool = False
        ):
            """
            初始化I2C总线
            
            参数:
                host (Union[str, int]): 主机标识
                scl (Union[str, int]): SCL引脚
                sda (Union[str, int]): SDA引脚
                freq (int): 频率,默认4000000
                use_locks (bool): 是否使用锁,默认False
            返回:
                (None): 无返回值
            """
            ...

        def __enter__(self) -> "I2C.Bus":
            """
            进入上下文管理器
            
            参数:
                无
            返回:
                (I2C.Bus): I2C总线对象
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            """
            退出上下文管理器
            
            参数:
                exc_type: 异常类型
                exc_val: 异常值
                exc_tb: 异常追踪
            返回:
                (None): 无返回值
            """
            ...

        def scan(self) -> list:
            """
            扫描I2C设备
            
            参数:
                无
            返回:
                (list): 设备地址列表
            """
            ...

        def start(self) -> None:
            """
            开始I2C传输
            
            参数:
                无
            返回:
                (None): 无返回值
            """
            ...

        def stop(self) -> None:
            """
            停止I2C传输
            
            参数:
                无
            返回:
                (None): 无返回值
            """
            ...

        def readinto(self, buf: _BUFFER_TYPE,  nack: bool = True) -> None:
            """
            读取数据到缓冲区
            
            参数:
                buf (_BUFFER_TYPE): 缓冲区
                nack (bool): 是否发送NACK，默认True
            返回:
                (None): 无返回值
            """
            ...

        def write(self, buf: _BUFFER_TYPE) -> None:
            """
            写入数据
            
            参数:
                buf (_BUFFER_TYPE): 要写入的数据
            返回:
                (None): 无返回值
            """
            ...

        def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
            """
            从指定地址读取数据
            
            参数:
                addr (int): 设备地址
                nbytes (int): 读取字节数
                stop (bool): 是否发送停止信号,默认True
            返回:
                (bytes): 读取的数据
            """
            ...

        def readfrom_into(self, addr: int, buf: _BUFFER_TYPE, stop: bool = True) -> None:
            """
            从指定地址读取数据到缓冲区
            
            参数:
                addr (int): 设备地址
                buf (_BUFFER_TYPE): 缓冲区
                stop (bool): 是否发送停止信号,默认True
            返回:
                (None): 无返回值
            """
            ...

        def writeto(self, addr: int, buf: _BUFFER_TYPE, stop: bool = True) -> None:
            """
            向指定地址写入数据
            
            参数:
                addr (int): 设备地址
                buf (_BUFFER_TYPE): 要写入的数据
                stop (bool): 是否发送停止信号,默认True
            返回:
                (None): 无返回值
            """
            ...

        def writevto(self, addr: int, vector: list, stop: bool = True) -> None:
            """
            向指定地址写入向量数据
            
            参数:
                addr (int): 设备地址
                vector (list): 向量数据
                stop (bool): 是否发送停止信号,默认True
            返回:
                (None): 无返回值
            """
            ...

        def readfrom_mem(self, addr: int, memaddr: int, nbytes: int, addrsize: int = 8) -> bytes:
            """
            从指定地址的内存读取数据
            
            参数:
                addr (int): 设备地址
                memaddr (int): 内存地址
                nbytes (int): 读取字节数
                addrsize (int): 地址大小,默认8
            返回:
                (bytes): 读取的数据
            """
            ...

        def readfrom_mem_into(self, addr: int, memaddr: int, buf: _BUFFER_TYPE, addrsize: int = 8) -> None:
            """
            从指定地址的内存读取数据到缓冲区
            
            参数:
                addr (int): 设备地址
                memaddr (int): 内存地址
                buf (_BUFFER_TYPE): 缓冲区
                addrsize (int): 地址大小,默认8
            返回:
                (None): 无返回值
            """
            ...

        def writeto_mem(self, addr: int, memaddr: int, buf: _BUFFER_TYPE, addrsize: int = 8) -> None:
            """
            向指定地址的内存写入数据
            
            参数:
                addr (int): 设备地址
                memaddr (int): 内存地址
                buf (_BUFFER_TYPE): 要写入的数据
                addrsize (int): 地址大小,默认8
            返回:
                (None): 无返回值
            """
            ...


    class Device(object):
        _bus: "I2C.Bus" = ...
        dev_id: int = ...
        _reg_bits: int = ...

        def __init__(self, bus: "I2C.Bus", dev_id: int, reg_bits: int = 8):
            """
            初始化I2C设备
            
            参数:
                bus (I2C.Bus): I2C总线对象
                dev_id (int): 设备ID
                reg_bits (int): 寄存器位数,默认8
            返回:
                (None): 无返回值
            """
            ...

        def write_readinto(self, write_buf: _BUFFER_TYPE, read_buf: _BUFFER_TYPE) -> None:
            """
            写入后读取数据到缓冲区
            
            参数:
                write_buf (_BUFFER_TYPE): 写入缓冲区
                read_buf (_BUFFER_TYPE): 读取缓冲区
            返回:
                (None): 无返回值
            """
            ...

        def read_mem(self, memaddr: int, num_bytes: Optional[int] = None, buf: Optional[_BUFFER_TYPE] = None) -> Optional[bytes]:
            """
            读取内存数据
            
            参数:
                memaddr (int): 内存地址
                num_bytes (Optional[int]): 读取字节数,默认None
                buf (Optional[_BUFFER_TYPE]): 缓冲区,默认None
            返回:
                (Optional[bytes]): 读取的数据
            """
            ...

        def write_mem(self, memaddr: int, buf: _BUFFER_TYPE):
            """
            写入内存数据
            
            参数:
                memaddr (int): 内存地址
                buf (_BUFFER_TYPE): 要写入的数据
            返回:
                (None): 无返回值
            """
            ...

        def read(self, nbytes: Optional[int] = None, buf: Optional[_BUFFER_TYPE] = None, stop: bool=True) -> Optional[bytes]:
            """
            读取数据
            
            参数:
                nbytes (Optional[int]): 读取字节数，默认None
                buf (Optional[_BUFFER_TYPE]): 缓冲区，默认None
                stop (bool): 是否发送停止信号，默认True
            返回:
                (Optional[bytes]): 读取的数据
            """
            ...

        def write(self, buf: _BUFFER_TYPE, stop: bool=True) -> None:
            """
            写入数据
            
            参数:
                buf (_BUFFER_TYPE): 要写入的数据
                stop (bool): 是否发送停止信号，默认True
            返回:
                (None): 无返回值
            """
            ...
