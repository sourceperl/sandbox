# Grove-LCD RGB Backlight 16x2 I2C

from machine import Pin, I2C
from utime import sleep_ms, sleep_us


# some class
class Grove_LCD_I2C(object):
    # I2C address
    LCD_ADDR = 0x3e
    RGB_ADDR = 0x62

    # Commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # Flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # Flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self, i2c, oneline=False, charsize=LCD_5x8DOTS):
        self.i2c = i2c
        self.disp_func = self.LCD_DISPLAYON # | 0x10
        if not oneline:
            self.disp_func |= self.LCD_2LINE
        elif charsize != 0:
            # For 1-line displays you can choose another dotsize
            self.disp_func |= self.LCD_5x10DOTS

        # Wait for display init after power-on
        sleep_ms(50)

        # send function set
        self.cmd(self.LCD_FUNCTIONSET | self.disp_func)
        sleep_us(4500)
        self.cmd(self.LCD_FUNCTIONSET | self.disp_func)
        sleep_us(150)
        self.cmd(self.LCD_FUNCTIONSET | self.disp_func)
        self.cmd(self.LCD_FUNCTIONSET | self.disp_func)

        # turn on the display
        self.disp_ctrl = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.display(True)

        # clear it
        self.clear()

        # set default text direction (left-to-right)
        self.disp_mode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.cmd(self.LCD_ENTRYMODESET | self.disp_mode)

    # set backlight to (R,G,B) (values from 0..255 for each)
    def setRGB(self, r, g, b):
        self.i2c.writeto_mem(self.RGB_ADDR, 0, bytes([0x00]))
        self.i2c.writeto_mem(self.RGB_ADDR, 1, bytes([0x20]))
        self.i2c.writeto_mem(self.RGB_ADDR, 2, bytes([b]))
        self.i2c.writeto_mem(self.RGB_ADDR, 3, bytes([g]))
        self.i2c.writeto_mem(self.RGB_ADDR, 4, bytes([r]))
        self.i2c.writeto_mem(self.RGB_ADDR, 8, bytes([0xaa]))

    def cmd(self, command):
        assert command >= 0 and command < 256
        command = bytearray([command])
        self.i2c.writeto_mem(self.LCD_ADDR, 0x80, bytearray([]))
        self.i2c.writeto_mem(self.LCD_ADDR, 0x80, command)

    def write_char(self, c):
        assert c >= 0 and c < 256
        c = bytearray([c])
        self.i2c.writeto_mem(self.LCD_ADDR, 0x40, c)

    def write(self, text):
        for char in text:
            if char == '\n':
                self.cursor_position(0, 1)
            else:
                self.write_char(ord(char))

    def cursor(self, state):
        if state:
            self.disp_ctrl |= self.LCD_CURSORON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)
        else:
            self.disp_ctrl &= ~self.LCD_CURSORON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)

    def cursor_position(self, col, row):
        col = (col | 0x80) if row == 0 else (col | 0xc0)
        self.cmd(col)

    def autoscroll(self, state):
        if state:
            self.disp_ctrl |= self.LCD_ENTRYSHIFTINCREMENT
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)
        else:
            self.disp_ctrl &= ~self.LCD_ENTRYSHIFTINCREMENT
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)

    def blink(self, state):
        if state:
            self.disp_ctrl |= self.LCD_BLINKON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)
        else:
            self.disp_ctrl &= ~self.LCD_BLINKON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)

    def display(self, state):
        if state:
            self.disp_ctrl |= self.LCD_DISPLAYON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)
        else:
            self.disp_ctrl &= ~self.LCD_DISPLAYON
            self.cmd(self.LCD_DISPLAYCONTROL  | self.disp_ctrl)

    def clear(self):
        self.cmd(self.LCD_CLEARDISPLAY)
        sleep_ms(2)

    def home(self):
        self.cmd(self.LCD_RETURNHOME)
        sleep_ms(2)