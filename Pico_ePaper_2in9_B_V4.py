# *****************************************************************************
# * | File        :	  Pico_ePaper-2.13-B_V4.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2022-08-22
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI
import framebuf
import utime


EPD_WIDTH       = 128
EPD_HEIGHT      = 296

class EPD_2in9_B_V4_Portrait:
    def __init__(self, spi=None, cs=17, dc=20, rst=21, busy=22):
        self.reset_pin = Pin(rst, Pin.OUT) if isinstance(rst, int) else rst
        self.busy_pin = Pin(busy, Pin.IN, Pin.PULL_UP) if isinstance(busy, int) else busy
        self.cs_pin = Pin(cs, Pin.OUT) if isinstance(cs, int) else cs
        self.dc_pin = Pin(dc, Pin.OUT) if isinstance(dc, int) else dc
        if EPD_WIDTH % 8 == 0:
            self.width = EPD_WIDTH
        else :
            self.width = (EPD_WIDTH // 8) * 8 + 8
        self.height = EPD_HEIGHT
        
        if spi is None:
            self.spi = SPI(0, baudrate=4000_000, sck=Pin(18), mosi=Pin(19))
        else:
            self.spi = spi
        
        
        self.buffer_balck = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_balck, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy, pin=', self.digital_read(self.busy_pin))
        timeout = 0
        while(self.digital_read(self.busy_pin) == 1): 
            self.delay_ms(100)
            timeout += 1
            if timeout > 200:
                print('busy timeout!')
                return
        print('busy release')
        self.delay_ms(20)
        
    def TurnOnDisplay(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xF7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()

    def TurnOnDisplay_Base(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xF4)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Fast(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Partial(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0x1C)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()


    def init(self):
        # EPD hardware init start
        self.reset()

        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data((self.height-1)%256)    
        self.send_data((self.height-1)//256)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.send_command(0x44) #set Ram-X address start/end position   
        self.send_data(0x00)
        self.send_data(self.width//8-1)   

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0x00)
        self.send_data(0x00) 
        self.send_data((self.height-1)%256)    
        self.send_data((self.height-1)//256)

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x05)	

        self.send_command(0x21) #  Display update control
        self.send_data(0x00)		
        self.send_data(0x80)	

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)	

        self.send_command(0x4E)   # set RAM x address count to 0
        self.send_data(0x00)
        self.send_command(0x4F)   # set RAM y address count to 0X199    
        self.send_data(0x00)    
        self.send_data(0x00)
        self.ReadBusy()
        
        return 0
    
    def init_Fast(self):
        # EPD hardware init start
        self.reset()

        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   	

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)

        self.send_command(0x22) # Load temperature value
        self.send_data(0xB1)		
        self.send_command(0x20)	
        self.ReadBusy()   

        self.send_command(0x1A) # Write to temperature register
        self.send_data(0x5a)		# 90		
        self.send_data(0x00)	
                    
        self.send_command(0x22) # Load temperature value
        self.send_data(0x91)		
        self.send_command(0x20)	
        self.ReadBusy()  

        self.send_command(0x01) #Driver output control      
        self.send_data((self.height-1)%256)    
        self.send_data((self.height-1)//256)
        self.send_data(0x00)

        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.send_command(0x44) #set Ram-X address start/end position   
        self.send_data(0x00)
        self.send_data(self.width//8-1)   

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0x00)
        self.send_data(0x00) 
        self.send_data((self.height-1)%256)    
        self.send_data((self.height-1)//256)	

        self.send_command(0x4E)   # set RAM x address count to 0
        self.send_data(0x00)
        self.send_command(0x4F)   # set RAM y address count to 0X199    
        self.send_data(0x00)    
        self.send_data(0x00)
        self.ReadBusy()	
        
        return 0
    
    def display(self): # ryimage: red or yellow image
        self.send_command(0x24)
        self.send_data1(self.buffer_balck)

        self.send_command(0x26)
        self.send_data1(self.buffer_red)

        self.TurnOnDisplay()

    def display_Fast(self): # ryimage: red or yellow image
        self.send_command(0x24)
        self.send_data1(self.buffer_balck)

        self.send_command(0x26)
        self.send_data1(self.buffer_red)

        self.TurnOnDisplay_Fast()

    def Clear(self):
        self.send_command(0x24)
        self.send_data1([0xFF] * self.height * int(self.width / 8))
        
        self.send_command(0x26)
        self.send_data1([0x00] * self.height * int(self.width / 8))
                                
        self.TurnOnDisplay()

    def display_Partial(self, Image, Xstart, Ystart, Xend, Yend):
        if((Xstart % 8 + Xend % 8 == 8 & Xstart % 8 > Xend % 8) | Xstart % 8 + Xend % 8 == 0 | (Xend - Xstart)%8 == 0):
            Xstart = Xstart // 8
            Xend = Xend // 8
        else:
            Xstart = Xstart // 8 
            if Xend % 8 == 0:
                Xend = Xend // 8
            else:
                Xend = Xend // 8 + 1
                
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height

        Xend -= 1
        Yend -= 1
	
        self.send_command(0x44)       # set RAM x address start/end, in page 35
        self.send_data(Xstart & 0xff)    # RAM x address start at 00h
        self.send_data(Xend & 0xff)    # RAM x address end at 0fh(15+1)*8->128 
        self.send_command(0x45)       # set RAM y address start/end, in page 35
        self.send_data(Ystart & 0xff)    # RAM y address start at 0127h
        self.send_data((Ystart>>8) & 0x01)    # RAM y address start at 0127h
        self.send_data(Yend & 0xff)    # RAM y address end at 00h
        self.send_data((Yend>>8) & 0x01)   

        self.send_command(0x4E)   # set RAM x address count to 0
        self.send_data(Xstart & 0xff)
        self.send_command(0x4F)   # set RAM y address count to 0X127    
        self.send_data(Ystart & 0xff)
        self.send_data((Ystart>>8) & 0x01)

        self.send_command(0x24)   #Write Black and White image to RAM
        for j in range(Height):
            for i in range(Width):
                if((j > Ystart-1) & (j < (Yend + 1)) & (i > Xstart-1) & (i < (Xend + 1))):
                    self.send_data(Image[i + j * Width])
        self.TurnOnDisplay_Partial()

    def sleep(self):
        self.send_command(0x10) 
        self.send_data(0x01)
        
        self.delay_ms(2000)
        self.module_exit()

        
if __name__=='__main__':
    epd = EPD_2in9_B_V4_Portrait()
    epd.Clear()
    
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0x00)
    epd.imageblack.text("Waveshare", 0, 10, 0x00)
    epd.imagered.text("ePaper-2.9-B-V4", 0, 25, 0xff)
    epd.imageblack.text("RPi Pico", 0, 40, 0x00)
    epd.imagered.text("Hello World", 0, 55, 0xff)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imagered.vline(10, 90, 40, 0xff)
    epd.imagered.vline(90, 90, 40, 0xff)
    epd.imageblack.hline(10, 90, 80, 0x00)
    epd.imageblack.hline(10, 130, 80, 0x00)
    epd.imagered.line(10, 90, 90, 130, 0xff)
    epd.imageblack.line(90, 90, 10, 130, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.init_Fast
    epd.imageblack.rect(10, 150, 40, 40, 0x00)
    epd.imagered.fill_rect(60, 150, 40, 40, 0xff)
    epd.display_Fast()
    epd.delay_ms(2000)
    
    epd.init()
    epd.Clear()
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()