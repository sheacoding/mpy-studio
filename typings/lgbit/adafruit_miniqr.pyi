from typing import List, Optional, Tuple

# QRCode 编码模式常量
M: int  # 掩模模式 M (Mask Pattern).
L: int  # 纠错等级 L (Low,低等级纠错能力).
H: int  # 纠错等级 H (High,高等级纠错能力).
Q: int  # 纠错等级 Q (Quartile,四分之一等级纠错能力).

# 伽罗瓦域指数表
EXP_TABLE: bytes

# 伽罗瓦域对数表
LOG_TABLE: bytes

class QRBitMatrix:
    """
    用于表示二维码的二维比特矩阵.
    支持访问和设置每个模块的状态(True/False).
    """

    def __init__(self, width: int, height: int):
        """
        初始化一个比特矩阵.

        参数:
            width (int): 矩阵宽度.
            height (int): 矩阵高度.
        """
        ...

    def __repr__(self) -> str:
        """
        返回矩阵的字符串表示(用于调试).

        返回:
            (str): 字符串表示.
        """
        ...

    def __getitem__(self, key: Tuple[int, int]) -> Optional[bool]:
        """
        获取指定位置的模块状态.

        参数:
            key (Tuple[int, int]): (x, y) 坐标.

        返回:
            (Optional[bool]): True 表示深色模块,False 表示浅色模块,None 表示未定义.
        """
        ...

    def __setitem__(self, key: Tuple[int, int], value: bool) -> None:
        """
        设置指定位置的模块状态.

        参数:
            key (Tuple[int, int]): (x, y) 坐标.
            value (bool): True 表示深色模块,False 表示浅色模块.
        """
        ...
    width: int
    height: int

class QRCode:
    """
    用于生成二维码的主类.
    支持添加数据、设置纠错等级、生成二维码矩阵等基本功能.
    """

    def __init__(self, *, qr_type: Optional[int] = None, error_correct: int = L):
        """
        初始化一个 QRCode 实例.

        参数:
            qr_type (Optional[int]): 二维码的版本类型(1~40),若不指定将自动推断.
            error_correct (int): 纠错等级,可选 L/M/Q/H.
        """
        ...

    @property
    def type(self) -> Optional[int]:
        """
        获取当前二维码的版本类型(1~40).
        """
        ...

    @property
    def ECC(self) -> int:
        """
        获取当前二维码的纠错等级.

        返回:
            (int): 纠错等级,可能的值为 L (低), M (中), Q (四分之一), H (高).
        """
        ...

    @property
    def matrix(self) -> QRBitMatrix:
        """
        获取二维码的矩阵表示.

        返回:
            (QRBitMatrix): 二维码的比特矩阵.
        """
        ...

    @property
    def module_count(self) -> int:
        """
        获取二维码模块数量(即边长).

        返回:
            (int): 二维码的模块数量(边长).
        """
        ...

    @property
    def data_cache(self) -> Optional[List[int]]:
        """
        获取已编码的数据缓存.

        返回:
            (Optional[List[int]]): 已编码的数据缓存.
        """
        ...

    @data_cache.setter
    def data_cache(self, value: Optional[List[int]]) -> None:
        """
        设置已编码的数据缓存.
        """
        ...

    def add_data(self, data: List[int]) -> None:
        """
        添加要编码的数据.

        参数:
            data (List[int]): 要编码的字节数据(列表形式).
        """
        ...

    def make(self, *, test: bool = False, mask_pattern: int = 0) -> None:
        """
        构建完整的二维码矩阵.

        参数:
            test (bool): 是否为测试模式.
            mask_pattern (int): 掩码模式编号(0~7).
        """
        ...
