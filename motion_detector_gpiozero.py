from gpiozero import LED
from gpiozero import MotionSensor

led = LED(3)
pir = MotionSensor(21)

led.off()
try:
    while True:
        pir.wait_for_motion()
        print('motion detected')
        led.on()
        pir.wait_for_no_motion()
        led.off()
        print('motion stopped')
except KeyboardInterrupt:
    print('exiting')