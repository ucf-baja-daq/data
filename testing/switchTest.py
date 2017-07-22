#switchTest
# connect pin 7 and ground to the two pins on the switch on the side
# you want to read ON

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # sets up a pull up resistor
# the switch doesnt run with a pull down configuration
# the two pins closer to what you want to be the ON position
# should be connected to give a TRUE value in that position

while True:
	input_state = GPIO.input(7)
	if input_state == False:     
		print('Switch on - TRUE')
		time.sleep(0.3)
	else:
		print('Switch off - False')
		time.sleep(0.3)
