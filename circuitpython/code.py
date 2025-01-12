import digitalio
import board

import os
import time

import rtc
import socketpool
import wifi

import adafruit_ntp

HVenable = digitalio.DigitalInOut(board.GP0)
HVenable.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.GP28)
led.direction = digitalio.Direction.OUTPUT


class NixieTube:
    def __init__(self, pin1, pin2, pin3, pin4):
        self.c1 = digitalio.DigitalInOut(pin1)
        self.c1.direction = digitalio.Direction.OUTPUT
        self.c2 = digitalio.DigitalInOut(pin2)
        self.c2.direction = digitalio.Direction.OUTPUT
        self.c3 = digitalio.DigitalInOut(pin3)
        self.c3.direction = digitalio.Direction.OUTPUT
        self.c4 = digitalio.DigitalInOut(pin4)
        self.c4.direction = digitalio.Direction.OUTPUT
        
        self.c1.value = True
        self.c2.value = True
        self.c3.value = True
        self.c4.value = True

    def display_digit(self, digit):
        # Convert the digit to a 4-bit binary representation
        binary_representation = '{0:04b}'.format(digit)
        print(binary_representation)
        self.c1.value = bool(int(binary_representation[3]))
        self.c2.value = bool(int(binary_representation[2]))
        self.c3.value = bool(int(binary_representation[1]))
        self.c4.value = bool(int(binary_representation[0 ]))


    def clear(self):
        """
        Turn off all segments of the Nixie tube.
        """
        self.c1.value = True
        self.c2.value = True
        self.c3.value = True
        self.c4.value = True
    
nixie1 = NixieTube(board.GP1, board.GP2, board.GP3, board.GP4)
nixie2 = NixieTube(board.GP5, board.GP6, board.GP7, board.GP8)
nixie3 = NixieTube(board.GP9, board.GP10, board.GP11, board.GP12)
nixie4 = NixieTube(board.GP13, board.GP14, board.GP15, board.GP16)
nixie5 = NixieTube(board.GP17, board.GP18, board.GP19, board.GP20)
nixie6 = NixieTube(board.GP21, board.GP22, board.GP26, board.GP27)

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
if wifi_ssid is None:
    print("WiFi credentials are kept in settings.toml, please add them there!")
    raise ValueError("SSID not found in environment variables")

try:
    wifi.radio.connect(wifi_ssid, wifi_password)
except ConnectionError:
    print("Failed to connect to WiFi with provided credentials")
    raise

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=-6, cache_seconds=3600)

rtc.RTC().datetime = ntp.datetime

HVenable.value = True

# After getting the time, do a quick cycle of all the digits to reveal any problems
for digit in range(10):
    led.value = not led.value
    nixie1.display_digit(digit)
    nixie2.display_digit(digit)
    nixie3.display_digit(digit)
    nixie4.display_digit(digit)
    nixie5.display_digit(digit)
    nixie6.display_digit(digit)
    time.sleep(0.3)  
    
nixie1.clear()  
nixie2.clear()
nixie3.clear()
nixie4.clear()
nixie5.clear()
nixie6.clear()

while True:
    print(time.localtime())
    timel = time.localtime()
    
    hour = "{:02}".format(timel.tm_hour)
    min = "{:02}".format(timel.tm_min)
    sec = "{:02}".format(timel.tm_sec)
    
    if timel.tm_sec % 2 == 0:
        led.value = True
    else:
        led.value = False
        
    nixie1.display_digit(int(hour[0]))
    nixie2.display_digit(int(hour[1]))
    nixie3.display_digit(int(min[0]))
    nixie4.display_digit(int(min[1]))
    nixie5.display_digit(int(sec[0]))
    nixie6.display_digit(int(sec[1]))
    
    time.sleep(0.01)


