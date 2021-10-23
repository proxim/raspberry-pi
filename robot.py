from gpiozero import Robot
from time import sleep

r = Robot(right = (13,19), left = (5,6))
sleep(7)
r.forward()
sleep(15)
r.right()
sleep(2)
r.left()
sleep(2)
r.stop()
sleep(1)
r.backward()
sleep(15)
r.stop()
print('done')