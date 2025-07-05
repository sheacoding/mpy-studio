import lcd_bus
from micropython import const
import machine
import st7789
import lvgl as lv
import task_handler
import time, gc, sys

# SCL 21
# SDA 47
# RST 45
# CS  41
# DC  40
# BLK 42


class Screen:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self._initialized = True
        self._jpeg_decoder = None
        self._display = None
        self._th = None
        self.canvas = None
        self._backlight = None

        try:
            if not lv.is_initialized():
                lv.init()
            spi_bus = machine.SPI.Bus(host=1, mosi=47, miso=-1, sck=21)
            self._display_bus = lcd_bus.SPIBus(
                spi_bus=spi_bus, freq=20000000, dc=40, cs=41
            )
            self._display = st7789.ST7789(
                data_bus=self._display_bus,
                display_width=240,
                display_height=320,
                color_space=lv.COLOR_FORMAT.RGB565,
                color_byte_order=st7789.BYTE_ORDER_BGR,
                rgb565_byte_swap=True,
                reset_pin=45,
                reset_state=st7789.STATE_LOW,
                backlight_pin=42,
            )
            self._display.set_power(True)
            self._display.init()
            self._display.set_backlight(100)
            print("屏幕初始化完成")
        except Exception as e:
            print(f"屏幕初始化失败: {type(e).__name__}")
            sys.print_exception(e)
            self.deinit()
            gc.collect()
            raise RuntimeError("屏幕初始化失败")

    def __del__(self):
        """析构函数,确保资源被释放"""
        print("__del__")
        self.deinit()

    def _init_canvas(self):
        if self.canvas is None:
            self.canvas = lv.obj()
            self._reset_canvas()
            lv.screen_load(self.canvas)
            if hasattr(task_handler.TaskHandler, "_current_instance"):
                task_handler.TaskHandler._current_instance = None
            if self._th is None:
                self._th = task_handler.TaskHandler()

    def _reset_canvas(self):
        if self.canvas is not None:
            self.canvas.set_style_bg_color(lv.color_make(0, 0, 0), 0)
            self.canvas.set_style_bg_opa(255, 0)

    def init(self):
        if self._display is not None:
            self._display.set_power(True)
            self._display.set_backlight(100)
        if self.canvas is None:
            self._init_canvas()

    def draw_img(self, x, y, w, h, img):
        if self.canvas is None:
            return None

        try:
            img_obj = lv.image(self.canvas)
            img_obj.set_pos(x, y)
            img_obj.set_size(w, h)

            if isinstance(img, str):
                # 先判断文件格式
                if not img.lower().endswith((".png", ".jpg", ".jpeg")):
                    return None

                # 读取文件数据
                with open(img, "rb") as f:
                    imgdata = f.read()

                if img.lower().endswith((".jpg", ".jpeg")):
                    # JPEG文件处理,使用esp-new-jpeg硬解码
                    try:
                        if self._jpeg_decoder is None:
                            import jpeg

                            self._jpeg_decoder = jpeg.Decoder(format="RGB565_LE")
                        info = self._jpeg_decoder.get_img_info(imgdata)
                        width, height = info[0], info[1]
                        rgb_data = self._jpeg_decoder.decode(imgdata)
                        if rgb_data is None:
                            print("JPEG解码失败: 未返回数据")
                            return None
                        img_dsc = lv.image_dsc_t(
                            {
                                "header": {
                                    "cf": lv.COLOR_FORMAT.RGB565,
                                    "w": width,
                                    "h": height,
                                    "stride": width * 2,
                                    "flags": 0,
                                    "magic": 0x19,
                                },
                                "data_size": len(rgb_data),
                                "data": rgb_data,
                            }
                        )
                        img_obj.set_src(img_dsc)
                    except Exception as e:
                        print(f"JPEG解码失败: {e}")
                        return None
                else:
                    # PNG文件处理 - 使用 LVGL 内置解码器
                    img_dsc = lv.image_dsc_t(
                        {"data_size": len(imgdata), "data": imgdata}
                    )
                    img_obj.set_src(img_dsc)
            else:
                img_obj.set_src(img)

            return img_obj

        except Exception as e:
            print(f"绘制图片失败: {e}")
            return None

    def draw_text(self, text="hello", line=0, color=0xFFFFFF):
        if self.canvas is None:
            return None

        try:
            y_pos = 10 + line * 30
            label = lv.label(self.canvas)
            label.set_text(text)
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            label.set_style_text_color(lv.color_make(r, g, b), 0)
            # label.set_style_text_font(lv.font_puhui_20_4, 0)
            label.align(lv.ALIGN.TOP_LEFT, 5, y_pos)
            return label
        except Exception as e:
            print(f"绘制文本失败: {e}")
            return None

    def clear(self):
        """清除 canvas 上的所有内容"""
        if self.canvas is None:
            return
        try:
            del self.canvas
            self._init_canvas()
            gc.collect()
        except Exception as e:
            print(f"清除画布失败: {type(e).__name__}")
            sys.print_exception(e)

    def deinit(self):
        if self._th is not None:
            del self._th
        if self._display is not None:
            del self._display
        if self._jpeg_decoder is not None:
            del self._jpeg_decoder
        if self.canvas is not None:
            del self.canvas

        self._initialized = False
        Screen._instance = None
        lv.deinit()
        gc.collect()
        print("[Screen]释放资源完成")


if __name__ == "__main__":
    screen = Screen()
    screen.init()
    screen.draw_text("123")
