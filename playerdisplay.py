import os
from display import Display

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class PlayerDisplay(Display):

    ADDRESS = 0x3C
    RST_PIN = 4

    FONT_FILE = "cellphone_6px.ttf"
    FONT_SIZE = 16

    LINE_HEIGHT = 8
    CHAR_WIDTH  = 6

    START_LEFT =  1
    START_TOP  = -4

    def __init__(self, font_dir="./"):
        self.oled = Adafruit_SSD1306.SSD1306_128_64(rst=PlayerDisplay.RST_PIN, i2c_address=PlayerDisplay.ADDRESS)
        self.oled.begin()
        self.oled.clear()
        self.oled.display()
        self.width = self.oled.width
        self.height = self.oled.height
        self.image = Image.new('1', (self.width, self.height)) # 1 = 1-bit color
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0) # TODO is this needed?
        font_file = os.path.join(font_dir, PlayerDisplay.FONT_FILE)
        self.font = ImageFont.truetype(font_file, PlayerDisplay.FONT_SIZE)

    # Return display width in pixels
    def get_width(self):
        return self.width

    # Return display height in pixels
    def get_height(self):
        return self.height

    # Return the number of characters that
    # can be displayed in one line
    def get_num_chars_per_line(self):
        return 21 # TODO calc this instead

    # Return the number of lines
    def get_num_lines(self):
        return 8 # TODO calc this instead

    # Render the given string in the given line
    # String should only contain ASCII and should
    # not exceed get_num_chars_per_line() length
    def draw_string(self, line, text, align=None):
        x = PlayerDisplay.START_LEFT
        y = PlayerDisplay.START_TOP + (line * PlayerDisplay.LINE_HEIGHT)
        self.draw.text((x, y), text[:self.get_num_chars_per_line()], font=self.font, fill=255)

    # Render the given char in the given line/pos
    def draw_char(self, line, pos, char):
        x = PlayerDisplay.START_LEFT + (pos * PlayerDisplay.CHAR_WIDTH)
        y = PlayerDisplay.START_TOP + (line * PlayerDisplay.LINE_HEIGHT)
        self.draw.text((x, y), char[:1], font=self.font, fill=255)

    def clear(self):
        self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=0)
        #self.oled.clear()
        #self.oled.display()

    def display(self):
        self.oled.image(self.image)
        self.oled.display()

    def cleanup(self):
        self.oled.clear()
        self.oled.display()
