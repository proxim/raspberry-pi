from gpiozero import Button, LED
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setwarnings(False)
p = GPIO.PWM(18,50)
button = Button(14)
led = LED(15)
print('hello')
button.wait_for_press()
led.on()
print('button pressed')
p.start(7.5)
try:
    while True:
        p.ChangeDutyCycle(2.5)
        time.sleep(10)
        p.ChangeDutyCycle(7.5)
        time.sleep(.2)
        
except KeyboardInterrupt:
    p.stop()
finally:
    GPIO.cleanup()