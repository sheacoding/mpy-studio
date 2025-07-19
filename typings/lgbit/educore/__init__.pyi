# 引脚
from educore.pin import pin
# LED灯
from educore.rgb import rgb
# 按键
from educore.button import button
# 蜂鸣器
from educore.speaker import speaker
# 声音传感器
from educore.sound import sound
# 光线传感器
from educore.light import light
# 磁力计
from educore.compass import compass
# 加速度传感器
from educore.accelerometer import accelerometer
# OLED屏幕
from educore.oled import OLED
# WIFI
from educore.wifi import WiFi
# MQTT
from educore.mqtt import MqttClient
# RFID
from educore.rfid import rfid
# 舵机
from educore.servo import servo
# DHT11温湿度传感器
from educore.dht import dht
# 超声波
from educore.ultrasonic import ultrasonic
# DS18B20温度传感器
from educore.ds18b20 import ds18b20

from typing import Dict, Any, Callable, Optional, Tuple

oled:OLED
wifi:WiFi
mqttclient:MqttClient

def set_dict_values_to_none(d: Dict[str, object]) -> None:
    """
    将字典中所有键的值设置为 None.

    参数:
        d (Dict[str, object]): 输入的字典.
    """
    ...

def get_dict_from_file(dict_file: str) -> Dict[str, str]:
    """
    从指定文件读取键值对并构造成字典.

    参数:
        dict_file (str): 文件路径.

    返回:
        (Dict[str, str]): 包含文件内容的字典.
    """
    ...

def get_dict_from_str(s: str) -> Dict[str, str]:
    """
    从字符串解析键值对并构造成字典.

    参数:
        s (str): 输入字符串,支持换行符或分号分隔.

    返回:
        (Dict[str, str]): 解析后的字典.
    """
    ...

def abs(num: float) -> float:
    """
    返回给定数字的绝对值.

    参数:
        num (float): 数字.

    返回:
        (float): 绝对值.
    """
    ...

__all__ = [
    "pin",
    "rgb",
    "button",
    "speaker",
    "sound",
    "light",
    "compass",
    "accelerometer",
    "rfid",
    "servo",
    "dht",
    "ultrasonic",
    "ds18b20",
    "oled",
    "wifi",
    "mqttclient",
    "set_dict_values_to_none",
    "get_dict_from_file",
    "get_dict_from_str",
    "abs",
]