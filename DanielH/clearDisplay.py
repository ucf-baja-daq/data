import time
import math
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

ON  = 0
OFF = 1

digits = (33,29,22,16)

def clear():
	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)








