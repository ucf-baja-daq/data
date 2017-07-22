import time
import math
import RPi.GPIO as GPIO
import SevenSeg
import sys
sys.path.insert(0, '/home/pi/ABElectronics_Python3_Libraries/ADCDifferentialPi')
from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import threading

# ADC Setup
channel = 1     # analog channel number (1-8 inclusive)
bitRate = 18    # programmable data rate 
                    # 18 (3.75 SPS) less per sec. but more accurate
                    # 16 (  15 SPS) --
                    # 14 (  60 SPS) --
                    # 12 ( 240 SPS) more per sec. but less accurate
                    
i2cAddr1 = 0x68 # these addresses are associated with the Address Config. 1
i2cAddr2 = 0x69

mph = 0

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

ON  = 0
OFF = 1

segments = (7,11,12,13,15,18,31,32)
digits = (33,29,22,16)

	#                e    d    dp   c    g    b    f    a
numbers = { ' ':[OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
	'0':[ON , ON , OFF, ON , OFF, ON , ON , ON ],
	'1':[OFF, OFF, OFF, ON , OFF, ON , OFF, OFF],
	'2':[ON , ON , OFF, OFF,  ON, ON , OFF, ON ],
	'3':[OFF, ON , OFF, ON , ON , ON , OFF, ON ],
	'4':[OFF, OFF, OFF, ON , ON , ON , ON , OFF],
	'5':[OFF, ON , OFF, ON , ON , OFF, ON , ON ],
	'6':[ON , ON , OFF, ON , ON , OFF, ON , ON ],
	'7':[OFF, OFF, OFF, ON , OFF, ON , ON , ON ],
	'8':[ON , ON , OFF, ON , ON , ON , ON , ON ],
	'9':[OFF, ON , OFF, ON , ON , ON , ON , ON ] }

numKeys = [' ','0','1','2','3','4','5','6','7','8','9']

# GPIO Setup
GPIO.setmode( GPIO.BOARD )
GPIO.setup( 7, GPIO.OUT )

text_file = open("hallSensor_Data.txt", "w")
initTime = time.time()

c = threading.Condition()
flag = 0

class sevSeg_Thread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		global mph
		global flag
		while True:
			print (int(mph))
			c.acquire()
			if flag == 0:
				flag = 1
				inputStr = str( int(mph) )
				length = len(inputStr)
				display = [0]*length
				actualDigits = [0]*length

				for i in range (0,length):
					display[i] = inputStr[i]           # putting input Number into display array

				k = 3
				for i in range (length - 1, -1, -1):
					actualDigits[i] = digits[k]
					k = k - 1

				i = 0
				for dig in actualDigits:
					onOFF_value = numbers[display[i]]

					j = 0
					for val in onOFF_value:
						GPIO.output( segments[j], val )
						j = j + 1

					GPIO.output(dig, True)
					time.sleep(0.0005)
					GPIO.output(dig, False)

					i = i + 1
				c.notify_all()
			else:
				c.wait()
			c.release()
		

class hallSensor_Thread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		global mph
		global flag
		t1 = 0
		t2 = 0
		flagMine = 0
		diameter = 14     # need to find the actual diameter !!!

		i2c_helper = ABEHelpers()
		bus = i2c_helper.get_smbus()
		adc = ADCDifferentialPi(bus, i2cAddr1, i2cAddr2, bitRate)
		while True:
			c.acquire()
			if flag == 1:
				flag = 0
				voltage = adc.read_voltage( channel )               # voltage output from hall sensor (either a pos. or neg. value)
				curTime = time.time() - initTime                    # calculates the current time from time acc. minus time started with

				if voltage < 0.0 and flagMine == 0:                     # if voltage is neg. and we have not passed by the magnet yet
					flagMine = 1
					t1 = t2                                             # stores the previous curent time from curTime
					t2 = curTime                                        # stores the current time in curTime
					rps = 1/(t2 - t1)                                   # revolutions per second
					mph = rps * (math.pi) * diameter * (3600/63360)     # conversion from rps to miles per second
					#mph = rps*60

					#print( str(curTime) + "," + str(voltage) + "," + str(mph) )
					#text_file.write( str(curTime) + "," + str(voltage) + "," + str(mph) + "\n" )

				elif voltage < 0.0 and flagMine == 1:                   # else if voltage is neg. but we are currently still passing by the magnet
					#print( str(curTime) + "," + str(voltage) )
					#text_file.write( str(curTime) + "," + str(voltage) + "\n" )
					temp = 1

				else:                                               # else the voltage is positive (meaning the magnet is not next the the hall sensor)
					flagMine = 0
					#print( str(curTime) + "," + str(voltage) )
					#text_file.write( str(curTime) + "," + str(voltage) + "\n" )

				#mph = mph + 1
				c.notify_all()
			else:
				c.wait()
			c.release()
		text_file.close()	

#########

def initDisplay():
	for seg in segments:
		GPIO.setup(seg, GPIO.OUT)
		GPIO.output(seg, False)

	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)

initDisplay()

a = sevSeg_Thread("nameA")
b = hallSensor_Thread("nameB")

b.start()
a.start()

a.join()
b.join()

