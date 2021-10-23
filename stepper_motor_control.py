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
