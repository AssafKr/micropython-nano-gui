# Nano-gui compatible wrapper for Waveshare 2.9" B V4
from machine import Pin, SPI
import framebuf
from Pico_ePaper_2in9_B_V4 import EPD_2in9_B_V4_Portrait

class EPD(framebuf.FrameBuffer):
    
    @staticmethod
    def rgb(r, g, b):
        return int((r > 127) or (g > 127) or (b > 127))
    
    def __init__(self, spi=None, cs=17, dc=20, rst=21, busy=22, landscape=False):
        self._epd = EPD_2in9_B_V4_Portrait(spi, cs, dc, rst, busy)
        self._landscape = landscape
        
        if landscape:
            self.width = 296
            self.height = 128
        else:
            self.width = 128
            self.height = 296
        
        # Buffer for nano-gui drawing (black)
        self._buffer = bytearray(296 * 128 // 8)
        # Buffer for red drawing in landscape coords
        self._red_buffer = bytearray(296 * 128 // 8)
        
        if landscape:
            super().__init__(self._buffer, self.width, self.height, framebuf.MONO_HLSB)
            # Red framebuffer in landscape coords
            self.red = framebuf.FrameBuffer(self._red_buffer, 296, 128, framebuf.MONO_HLSB)
        else:
            super().__init__(self._buffer, self.width, self.height, framebuf.MONO_HLSB)
            self.red = framebuf.FrameBuffer(self._red_buffer, 128, 296, framebuf.MONO_HLSB)
        
        self._epd.imagered.fill(0x00)
        self._epd.Clear()
        self._epd.init_Fast()
    
    def _rotate_buffer(self, src, dst, invert=False):
        """Rotate landscape buffer to portrait"""
        for i in range(len(dst)):
            dst[i] = 0
        
        for ly in range(128):
            for lx in range(296):
                src_byte = (ly * 296 + lx) // 8
                src_bit = 7 - (lx % 8)
                pixel = (src[src_byte] >> src_bit) & 1
                
                px = ly
                py = 295 - lx
                
                dst_byte = (py * 128 + px) // 8
                dst_bit = 7 - (px % 8)
                
                if invert:
                    if not pixel:
                        dst[dst_byte] |= (1 << dst_bit)
                else:
                    if pixel:
                        dst[dst_byte] |= (1 << dst_bit)
    
    def show(self):
        """Update display with rotation and color inversion"""
        if self._landscape:
            # Rotate black buffer (inverted for correct colors)
            self._rotate_buffer(self._buffer, self._epd.buffer_balck, invert=True)
            # Rotate red buffer (not inverted - 1=red)
            self._rotate_buffer(self._red_buffer, self._epd.buffer_red, invert=False)
        else:
            dst = self._epd.buffer_balck
            for i in range(len(self._buffer)):
                dst[i] = self._buffer[i] ^ 0xff
            # Copy red buffer directly
            red_dst = self._epd.buffer_red
            for i in range(len(self._red_buffer)):
                red_dst[i] = self._red_buffer[i]
        
        self._epd.display_Fast()
    
    def wait_until_ready(self):
        pass
