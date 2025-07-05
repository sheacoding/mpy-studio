from typing import Any, Optional
import lvgl as lv
import lcd_bus
import display_driver_framework

STATE_HIGH: int
STATE_LOW: int
STATE_PWM: int

BYTE_ORDER_RGB: int
BYTE_ORDER_BGR: int

class ST7789(display_driver_framework.DisplayDriver):
    _ORIENTATION_TABLE: tuple[int, ...]

    def __init__(
        self,
        data_bus: Any,
        display_width: int,
        display_height: int,
        frame_buffer1: Optional[Any] = ...,  # Could be memoryview or similar
        frame_buffer2: Optional[Any] = ...,
        reset_pin: Optional[int] = ...,
        reset_state: int = ...,
        power_pin: Optional[int] = ...,
        power_on_state: int = ...,
        backlight_pin: Optional[int] = ...,
        backlight_on_state: int = ...,
        offset_x: int = ...,
        offset_y: int = ...,
        color_byte_order: int = ...,
        color_space: int = ...,  # lv.COLOR_FORMAT
        rgb565_byte_swap: bool = ...,
    ) -> None: ... 