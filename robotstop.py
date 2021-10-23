from gpiozero import Robot
from time import sleep

r = Robot(right = (13,19), left = (5,6))
r.stop()