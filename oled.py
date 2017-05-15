#!/usr/bin/env python3
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('cellphone_varwidth.ttf', 16)
font = ImageFont.truetype('cellphone_6px.ttf', 16)

#draw.line((0, 10, 128, 10), fill=255)
#draw.line((0, 54, 128, 54), fill=255)
#draw.point((64,32), fill=255)

#                   012345678901234567891
draw.text((2, -4), "  Audio Book Player  ", font=font, fill=255)
draw.text((2,  4), "---------------------", font=font, fill=255)
draw.text((2, 12), "12/114            85%", font=font, fill=255)
draw.text((2, 20), "    8:23 / 15:67     ", font=font, fill=255)
draw.text((2, 28), "    Stephen King     ", font=font, fill=255)
draw.text((2, 36), "   The Dark Tower    ", font=font, fill=255)
draw.text((2, 44), "---------------------", font=font, fill=255)
draw.text((2, 52), "MENU  <<  |>  >>  VOL", font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
