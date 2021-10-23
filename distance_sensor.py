import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 24
ECHO = 23

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print('waiting for sensor')
time.sleep(1.5)

GPIO.output(TRIG, True)
time.sleep(.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == 0:
    start = time.time()
while GPIO.input(ECHO) == 1:
    end = time.time()

duration = end-start
distance = duration * 17150
distance = round(distance, 2)

print('Distance: ', distance, 'cm')

GPIO.cleanup()