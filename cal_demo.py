# Calendar demo - LANDSCAPE with RED (properly rotated)
from color_setup import ssd
from gui.core.writer import Writer
from gui.core.nanogui import refresh
import gui.fonts.arial10 as font
from extras.widgets.calendar import Calendar
from gui.widgets.label import Label

WHITE = 1
BLACK = 0

wri = Writer(ssd, font, verbose=False)
wri.set_clip(True, True, False)

print("Drawing landscape calendar...")
refresh(ssd, True)

# Calendar on left
cal = Calendar(wri, 12, 15, 16, WHITE, BLACK, WHITE, WHITE, WHITE, True, True)

# Labels on right
Label(wri, 12, 175, "December 2024")
Label(wri, 32, 175, "Landscape Mode")
Label(wri, 55, 175, "nano-gui + red")
Label(wri, 95, 175, "Waveshare 2.9B")

# Draw red in LANDSCAPE coords using ssd.red - more padding
ssd.red.fill(0x00)  # Clear red
ssd.red.rect(8, 8, 280, 112, 0xff)  # Red border with more margin
ssd.red.rect(9, 9, 278, 110, 0xff)
ssd.red.fill_rect(175, 68, 100, 3, 0xff)  # Red line
ssd.red.text("E-PAPER", 200, 78, 0xff)

# Update display (this rotates both black and red)
print("Updating...")
ssd.show()
print("Done!")
