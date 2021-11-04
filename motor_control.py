import RPi.GPIO as GPIO
import time

# connect in order of ln1 -> ln4
STEPPER_PINS = (26, 19, 13, 6)

CCW_SEQ = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]
CW_SEQ = CCW_SEQ[::-1]

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def cleanup(stepper=None):
    if stepper:
        stepper.reset_state()
    GPIO.cleanup()
    
class StepperMotor:
    """
    Interface for 5V DC 28BYJ-48 Servo Motor
    """
    def __init__(self, pins, delay=.001):
        self.pins = pins
        self.delay = delay # in seconds
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def set_state(self, pin_statuses):
        for i, pin in enumerate(STEPPER_PINS):
            GPIO.output(pin, pin_statuses[i])

    def reset_state(self):
        self.set_state([0, 0, 0, 0])
        
    def cycle(self, state_seq):
        for pins_state in state_seq:
            self.set_state(pins_state)
            time.sleep(self.delay) 
    
    def rotate(self, degrees, state_seq):
        # 8 cycles/revolution, 1:64 gear ratio, 1 revolution/360 degrees
        for _ in range(degrees * 8 * 64 // 360):
            self.cycle(state_seq)
    
    def rotate_cw(self, degrees=360):
        self.rotate(degrees, CW_SEQ)
    
    def rotate_ccw(self, degrees=360):
        self.rotate(degrees, CCW_SEQ)

class DCMotor():
    """ Class to control DC motor via L298n motor controller
    6 methods 1. __init__ 2. forward
    3.backward 4.stop 5 .brake 6.cleanup"""

    def __init__(self, pin_one, pin_two,
                 pwm_pin, freq=50, name='DC Motor'):
        """ init method
        (1) pin_one, type=int,  GPIO pin connected to IN1 or IN3
        (2) Pin two type=int, GPIO pin connected to IN2 or IN4
        (3) pwm_pin type=int, GPIO pin connected to EnA or ENB
        (4) freq in Hz default 50
        (5) name, type=string, name attribute
        """
        self.name = name
        self.pin_one = pin_one
        self.pin_two = pin_two
        self.pwm_pin = pwm_pin
        self.freq = freq

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_one, GPIO.OUT)
        GPIO.setup(self.pin_two, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.my_pwm = GPIO.PWM(self.pwm_pin, self.freq)
        self.last_pwm = 0
        self.my_pwm.start(self.last_pwm)


    def forward(self, duty_cycle=50):
        """ Move motor forwards passed duty cycle for speed control """
        GPIO.output(self.pin_one, True)
        GPIO.output(self.pin_two, False)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def backward(self, duty_cycle=50):
        """ Move motor backwards passed duty cycle for speed control"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, True)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def stop(self, duty_cycle=0):
        """ Stop motor"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, False)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def brake(self, duty_cycle=100):
        """ brake motor"""
        GPIO.output(self.pin_one, True)
        GPIO.output(self.pin_two, True)
        if duty_cycle != self.last_pwm:
            self.my_pwm.ChangeDutyCycle(duty_cycle)
            self.last_pwm = duty_cycle

    def cleanup(self, clean_up=False):
        """ cleanup all GPIO connections used in event of error by lib user"""
        GPIO.output(self.pin_one, False)
        GPIO.output(self.pin_two, False)
        self.my_pwm.ChangeDutyCycle(0)
        if clean_up:
            GPIO.cleanup()

if __name__ == '__main__':
    
    setup()

    stepper = StepperMotor(STEPPER_PINS)
    
    stepper.rotate_cw(90)
    stepper.rotate_ccw(90)

    cleanup()

#try:
#    pass
#except KeyboardInterrupt:
#    print('keyboard interrupted')
