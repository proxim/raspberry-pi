import time
import RPi.GPIO as GPIO
from pygame_display import *
from motor_control import DCMotor

# motor controller 1 pins
MC1_PWM1 = 23
MC1_LN1 = 25
MC1_LN2 = 8

MC1_LN3 = 7
MC1_LN4 = 1
MC1_PWM2 = 24

# motor controller 2 pins
MC2_LN1 = 5
MC2_LN2 = 6
MC2_PWM1 = 13

GPIO.setmode(GPIO.BCM)
    
if __name__ == '__main__':
    
    # setup pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 800))
    pygame.display.set_caption('OEDK Data Visualization')
    
    # set up motors
    low_motor = DCMotor(MC1_LN2, MC1_LN1, MC1_PWM1)
    mid_motor = DCMotor(MC1_LN3, MC1_LN4, MC1_PWM2)
    high_motor = DCMotor(MC2_LN2, MC2_LN1, MC2_PWM1)
    
    DIST_CONST = 1
    DIST_CONST_OR = .8
    TIME_BTN_STATS = 7
    
    # sample data (hardcoded for now)
    stats = [{
            'filename': 'graphics/pct_fem_users_2019-2021.png', # the filename doesn't reflect data
            'data': (37.39, 36.97, 42.07),
            'start_axis': 0.0,
            'end_axis': 50.0
        }, {
            'filename': 'graphics/num_tour_visitors_2015-2017.png',
            'data': (2552, 5212, 5821),
            'start_axis': 0.0,
            'end_axis': 7000.0
        }
    ]
    idx = 0

    running = True
    while running:
        screen.fill(WHITE)
        
        current_stat = stats[idx]
        print(current_stat)
        
        # change title + axis
        background = Image(current_stat['filename'])
        background.draw(screen)
        print('Changing background img')
        
        # update screen
        pygame.display.update()
        print('Updated screen')
        
        time.sleep(.5)
        
        # get the stats, and convert them into percentages of the entire screen
        distances = current_stat['data']
        start = current_stat['start_axis']
        end = current_stat['end_axis']
        pct_distances = map(lambda dist: (dist - start) / (end - start), distances) 
        low, mid, high = pct_distances
        
        # move motors
        low_motor.move(low, DIST_CONST_OR)

        mid_motor.move(mid, DIST_CONST)
        
        high_motor.move(high, DIST_CONST)

        # delay until next statistic
        time.sleep(TIME_BTN_STATS)
        
        # move motors back
        low_motor.move_back(low, DIST_CONST_OR)

        mid_motor.move_back(mid, DIST_CONST)
    
        high_motor.move_back(high, DIST_CONST)
        
        time.sleep(2)


        # increment index
        idx = 0 if idx == len(stats) - 1 else idx + 1
        
        # check pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
            
            
            if event.type == pygame.QUIT:
                print('Quitting...')
                running = False
                # cleanup
                for motor in (low_motor, mid_motor, high_motor):
                    motor.stop(0)
                GPIO.cleanup()
                pygame.quit()
          

        
