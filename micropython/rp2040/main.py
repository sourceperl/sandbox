#
# Raspberry Pi Pico test: display random number
#

from machine import I2C, Pin
from utime import sleep
import urandom
from grove_lcd_rgb_i2c import Grove_LCD_RGB_I2C

# some const
I2C_ID = 0
I2C_SDA = 0
I2C_SCL = 1

# init I2C bus
i2c = I2C(I2C_ID, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL))
# init LCD display
lcd = Grove_LCD_RGB_I2C(i2c)

# debug: scan I2C bus
#print('node(s) on I2C bus:', [hex(i) for i in i2c.scan()])

# turn on RGB backlight
lcd.setRGB(0x80, 0x80, 0x20)

# display the random number
lcd.home()
lcd.write('Random number:')

# main loop
while True:
    lcd.cursor_position(0, 1)
    lcd.write('{:^16d}'.format(urandom.randint(1, 49)))
    sleep(0.8)
