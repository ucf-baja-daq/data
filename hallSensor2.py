import time
import math
import RPi.GPIO as GPIO

import SevenSeg

import sys
sys.path.insert(0, '/home/pi/ABElectronics_Python3_Libraries/ADCDifferentialPi')

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers

mph = 0
flagThread = 0
killH = False

def getMph():
	global mph
	return mph

def getFlag():
	global flagThread
	return flagThread

def killHall():
	global killH
	killH = True

t1 = 0
t2 = 0

def hallSen():
	# ADC Setup
	channel = 1     # analog channel number (1-8 inclusive)
	bitRate = 12    # programmable data rate 
		            # 18 (3.75 SPS) less per sec. but more accurate
		            # 16 (  15 SPS) --
		            # 14 (  60 SPS) --
		            # 12 ( 240 SPS) more per sec. but less accurate
		            
	i2cAddr1 = 0x68 # these addresses are associated with the Address Config. 1
	i2cAddr2 = 0x69

	text_file = open("hallSensor_Data_2.txt", "w")
	initTime = time.time()

	global t1
	global t2
	flag = 0
	diameter = 14     # need to find the actual diameter !!!

	i2c_helper = ABEHelpers()
	bus = i2c_helper.get_smbus()
	adc = ADCDifferentialPi(bus, i2cAddr1, i2cAddr2, bitRate)

	global mph
	global flagThread
	global killH

	while True:
		if killH == True:
			text_file.close()
			time.sleep(10)
		else:
			voltage = adc.read_voltage( channel )               # voltage output from hall sensor (either a pos. or neg. value)
			curTime = time.time() - initTime                    # calculates the current time from time acc. minus time started with

			if voltage < 0.0 and flag == 0:                     # if voltage is neg. and we have not passed by the magnet yet
				flag = 1
				t1 = t2                                             # stores the previous curent time from curTime
				t2 = curTime                                        # stores the current time in curTime
				rps = 1/(t2 - t1)                                   # revolutions per second
				flagThread = 1
				mph = rps * (math.pi) * diameter * (3600/63360)     # conversion from rps to miles per second
				rpm = rps * 60
				flagThread = 0
				#mph = rps*60

				#print( str(curTime) + "," + str(voltage) + "," + str(mph) )
				text_file.write( str(curTime) + "," + str(rpm) + "\n" )
				text_file.flush()

			elif voltage < 0.0 and flag == 1:                   # else if voltage is neg. but we are currently still passing by the magnet
				#print( str(curTime) + "," + str(voltage) )
				#text_file.write( str(curTime) + "," + str(voltage) + "\n" )
				filler = 0

			else:                                               # else the voltage is positive (meaning the magnet is not next the the hall sensor)
				flag = 0
				#print( str(curTime) + "," + str(voltage) )
				#text_file.write( str(curTime) + "," + str(voltage) + "\n" )

		    #time.sleep( 0.0100 )

	text_file.close()
