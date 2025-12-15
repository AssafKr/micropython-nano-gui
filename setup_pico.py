#!/usr/bin/env python3
"""
Setup script for Waveshare 2.9" B V4 e-paper with nano-gui on Raspberry Pi Pico

Run from project root:
    python setup_pico.py

Requires: mpremote installed (pip install mpremote)
"""

import subprocess
import sys

def run(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("=== Setting up Pico for Waveshare 2.9\" B V4 e-paper ===\n")
    
    # Core driver files
    print("Uploading driver files...")
    run("mpremote cp Pico_ePaper_2in9_B_V4.py :Pico_ePaper_2in9_B_V4.py")
    run("mpremote cp epd29b_nanogui.py :epd29b_nanogui.py")
    run("mpremote cp color_setup.py :color_setup.py")
    
    # nano-gui core
    print("\nUploading nano-gui core...")
    run("mpremote mkdir :gui 2>nul")
    run("mpremote mkdir :gui/core 2>nul")
    run("mpremote mkdir :gui/widgets 2>nul")
    run("mpremote mkdir :gui/fonts 2>nul")
    
    run("mpremote cp gui/core/__init__.py :gui/core/__init__.py")
    run("mpremote cp gui/core/nanogui.py :gui/core/nanogui.py")
    run("mpremote cp gui/core/writer.py :gui/core/writer.py")
    run("mpremote cp gui/core/colors.py :gui/core/colors.py")
    run("mpremote cp gui/core/fplot.py :gui/core/fplot.py")
    
    run("mpremote cp gui/widgets/__init__.py :gui/widgets/__init__.py")
    run("mpremote cp gui/widgets/label.py :gui/widgets/label.py")
    run("mpremote cp gui/widgets/meter.py :gui/widgets/meter.py")
    run("mpremote cp gui/widgets/dial.py :gui/widgets/dial.py")
    run("mpremote cp gui/widgets/led.py :gui/widgets/led.py")
    run("mpremote cp gui/widgets/scale.py :gui/widgets/scale.py")
    run("mpremote cp gui/widgets/textbox.py :gui/widgets/textbox.py")
    
    # Fonts
    print("\nUploading fonts...")
    run("mpremote cp gui/fonts/arial10.py :gui/fonts/arial10.py")
    run("mpremote cp gui/fonts/arial35.py :gui/fonts/arial35.py")
    run("mpremote cp gui/fonts/arial_50.py :gui/fonts/arial_50.py")
    run("mpremote cp gui/fonts/freesans20.py :gui/fonts/freesans20.py")
    run("mpremote cp gui/fonts/font6.py :gui/fonts/font6.py")
    run("mpremote cp gui/fonts/font10.py :gui/fonts/font10.py")
    run("mpremote cp gui/fonts/courier20.py :gui/fonts/courier20.py")
    
    # Calendar extras (optional)
    print("\nUploading calendar extras...")
    run("mpremote mkdir :extras 2>nul")
    run("mpremote mkdir :extras/widgets 2>nul")
    run("mpremote cp extras/date.py :extras/date.py")
    run("mpremote cp extras/parse2d.py :extras/parse2d.py")
    run("mpremote cp extras/widgets/grid.py :extras/widgets/grid.py")
    run("mpremote cp extras/widgets/calendar.py :extras/widgets/calendar.py")
    
    print("\n=== Setup complete! ===")
    print("\nTest with:")
    print("  mpremote run cal_demo.py")

if __name__ == "__main__":
    main()

