import RPi.GPIO as GPIO
import time

LED = 3
sensor = 21

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(sensor, GPIO.IN)

setup()
try:
    while True:
        GPIO.output(LED, False)
        time.sleep(.1)
        if GPIO.input(sensor) == 1:
            print('motion detected')
            GPIO.output(LED, True)
            time.sleep(1)
        else:
            GPIO.output(LED, False)
except KeyboardInterrupt:
    GPIO.output(LED, False)
    GPIO.cleanup()
    print('keyboard interrupted')