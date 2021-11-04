import time
import RPi.GPIO as GPIO
from pygame_display import *
from motor_control import DCMotor

# motor controller 1 pins
MC1_PWM1 = 1
MC1_LN1 = 2
MC1_LN2 = 3
MC1_LN3 = 4
MC1_LN4 = 5
MC1_PWM2 = 6

# motor controller 2 pins
MC2_LN1 = 7
MC2_LN2 = 8
MC2_PWM1 = 9

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('OEDK Data Visualization')

    # setup
    low_motor = DCMotor(MC1_LN1, MC1_LN2, MC1_PWM1, name='Lower Motor')
    mid_motor = DCMotor(MC1_LN3, MC1_LN4, MC1_PWM2, name='Middle Motor')
    high_motor = DCMotor(MC2_LN1, MC2_LN2, MC2_PWM1, name='Highest Motor')
    
    running = True
    while running:
        screen.fill(WHITE)

        # change title + axis
        background = Image('graphics/pct_fem_users_2019-2021.png')
        background.draw(screen)
        
        # update screen
        pygame.display.update()

        # move motors
        low_motor.forward()
        time.sleep(5)

        # cycle screen


        # check pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()