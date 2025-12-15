# color_setup.py - LANDSCAPE mode
from machine import Pin, SPI
import gc
from epd29b_nanogui import EPD as SSD

spi = SPI(0, baudrate=4000_000, sck=Pin(18), mosi=Pin(19))
gc.collect()

ssd = SSD(
    spi=spi,
    cs=17,
    dc=20,
    rst=21,
    busy=22,
    landscape=True  # 296x128 landscape
)
