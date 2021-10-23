from rpi_ws281x import PixelStrip, Color
from time import sleep

# you must do: sudo pip install rpi_ws281x
# in the terminal before you can run this
# and you can only run this with the command
# sudo python led_strip.py
# in the terminal; it will not work in an IDE
# tutorial is at https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

# config
LED_COUNT = 23 # if not using an external power source for leds try to only use a max of 30 connected LEDs
LED_PIN = 18 # this is the pin to plug in the green wire (not the ground/5v wire)
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255 # 255 is the max brightness
LED_INVERT = False
LED_CHANNEL = 0
green = Color(0,255,0)
red = Color(255, 0, 0)
black = Color(0,0,0)

def green_strip(): # turns entire led strip green
    for x in range(LED_COUNT):
        strip.setPixelColor(x, green)
    strip.show()
def red_strip(): # turns entire led strip red
    for x in range(LED_COUNT):
        strip.setPixelColor(x, red)
    strip.show()
def clear_strip(): # turns off entire led strip
    for x in range(LED_COUNT):
        strip.setPixelColor(x, black)
    strip.show()
def wheel(pos):
    #Generate rainbow colors across 0-255 positions
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
def rainbow_cycle(strip, wait_ms=20, iterations=1):
    # draws a raindow that cycles across all leds
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        sleep(wait_ms/1000.0)

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
if __name__ == "__main__":
    try:
        while True:
            rainbow_cycle(strip)
    except KeyboardInterrupt:
        clear_strip()
