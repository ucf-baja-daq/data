# main Data Acqusition code
# runs on RPi boot

# we want this code to run on the pi's boot
# what should run on boot
#	-speedometer

# what should run via toggle switches
#	-CVT/gearbox data collection
#	-strain gauge data collection

import threading
import time
import math
import sharedValues
from timeit import default_timer as timer 

# flag to exit the program
exitFlag = 0

import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # IO 21; sets up a pull up resistor
GPIO.setup(38, GPIO.OUT) #IO 20 led 1
GPIO.setup(36, GPIO.OUT) #IO 16 led 2

GPIO.output(38, GPIO.LOW)
GPIO.output(36, GPIO.LOW)

hallLedPins = [38, 36]

segments = [7,21,12,23,15,18,31,32]
digits = [33,29,22,16]

speedNumber = 4444

ON = 0
OFF = 1

# the switch doesnt run with a pull down configuration
# the two pins closer to what you want to be the ON position
# should be connected to give a TRUE value in that position


class HallThread (threading.Thread):
	
	# initiate myThread object
	# threadID hallSensor position ("cvt" or "sec")
	# name - thread name 
	def __init__(self, threadID, name, counter, pinNumber, hallSensor_Num, diameter):
		threading.Thread.__init__(self)
		print("Initializing Hall Sensor on pin " + str(pinNumber) + ".")
		self.threadID = threadID
		self.name = name
		self.pinNumber = pinNumber
		self.runningFlag = 1
		self.ledPin = hallLedPins[hallSensor_Num - 1]
		
		self.isHallSenWithBoard = False
		
		# setup input pin for hallsensor
		GPIO.setup( pinNumber, GPIO.IN )
		
		# open file to write to
		# based on pin number and counter
		self.file_str = "data/hallSen_Data"+ str(pinNumber) + "_" + str(counter) + ".txt"
		self.text_file = open(self.file_str, "w")
		
		# initial time for time vector
		# self.initTime = time.time()
		self.initTime = timer()
		
		# initialize 
		self.t1 = 0
		self.t2 = 0
		self.hallFlag = 0
		self.gearRatio = 11.5
		
		print("Done.\n")
		
		
		
	def run(self):
		print("Running hall sensor on pin " + str(self.pinNumber) + ".")
		print("Writing to " + self.file_str)
		# while switch is toggled on
		
		global speedNumber
		self.counter = 0
		
		while self.runningFlag == 1:
			self.input_hallSen = GPIO.input( self.pinNumber )
			# self.curTime = time.time() - self.initTime
			self.curTime = timer() - self.initTime
			
			if self.input_hallSen == self.isHallSenWithBoard and self.hallFlag == 0:
				self.hallFlag = 1
				self.t1 = self.t2													# stores the previous current time from curTime
				self.t2 = self.curTime											# stores the current time in curTime
				self.rpm = 60/(self.t2 - self.t1)
				
				#sharedValues.setSpeed(int(self.rpm))
				speedNumber = int(self.rpm)
				
				GPIO.output(self.ledPin, GPIO.HIGH)
				#print(self.name + " - " + str(self.curTime) + "," + str(self.rpm))
				self.endTime = timer() - self.initTime
				if self.counter > 9:
					self.counter = 0
					self.text_file.flush()
				else:
					self.text_file.write( str(self.curTime) + "," + str(self.rpm) + "\n" )
					self.counter += 1
				#self.text_file.flush()
				GPIO.output(self.ledPin, GPIO.LOW)
			elif self.input_hallSen == self.isHallSenWithBoard and self.hallFlag == 1:
				self.filler = 0
			
			else:
				self.hallFlag = 0
		
		self.text_file.write(str(timer()-self.initTime))
		self.text_file.flush()
		self.text_file.close()
	
	def setFlag(self, flag):
		self.runningFlag = flag
		
class SevenSegThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		print("Initializing Seven Segment Display.")
		self.threadID = threadID
		self.name = name
		
		#					  e    d    dp   c    g    b    f    a
		self.numbers = { ' ':[OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
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
						 
		self.numKeys = [' ','0','1','2','3','4','5','6','7','8','9']
		
		for seg in segments:
			GPIO.setup(seg, GPIO.OUT)
			GPIO.output(seg, False);
			
		for dig in digits:
			GPIO.setup(dig, GPIO.OUT)
			GPIO.output(dig, False)
			
		self.num = 0
		self.length = 0
		
		self.inputStr = str( int(self.num) )
		
		self.length = len(self.inputStr)
		self.display = [0]*self.length
		self.actualDigits = [0]*self.length
		
		for i in range (0, self.length):
			self.display[i] = self.inputStr[i]
			
		self.k = 3
		for i in range(self.length - 1, -1, -1):
			self.actualDigits[i] = digits[self.k]
			self.k = self.k - 1
					
		print("Seven Seg SetUp: Done.\n")	
		
	def run(self):
		
		global speedNumber
		
		prevNum = 0
		
		stTime = timer()
		
		while True:
			#if hallSensor1.getFlag() == 0:
			
			#prevNum = self.num
			#if prevNum != 0:
			if timer() - stTime > 1.0:
				stTime = timer()
				self.num = speedNumber
			
			prevNum = self.num
				#self.num=1
			#else:
			#	num = num
				#if( not(int(num) % 2) ):
			self.inputStr = str( int(self.num) )
				#print(inputStr)
			self.length = len(self.inputStr)
			self.display = [0]*self.length
			self.actualDigits = [0]*self.length

			for i in range (0,self.length):
				self.display[i] = self.inputStr[i]           # putting input Number into display array

			self.k = 3
			for i in range (self.length - 1, -1, -1):
				self.actualDigits[i] = digits[self.k]
				self.k = self.k - 1
			#self.num = speedNumber
			i = 0
			for dig in self.actualDigits:
					
				onOFF_value = self.numbers[self.display[i]]

				j = 0
				for val in onOFF_value:
					GPIO.output( segments[j], val )
					j = j + 1

				GPIO.output(dig, True)
				time.sleep(0.0005)
				GPIO.output(dig, False)

				i = i + 1
	
############	
	
def start():
	global exitFlag
	global hallLedPins
		
	counter = 0
	switchFlag = 0

	#startup LED
	GPIO.output(38, GPIO.HIGH)
	GPIO.output(36, GPIO.HIGH)
	time.sleep(3)
	GPIO.output(38, GPIO.LOW)
	GPIO.output(36, GPIO.LOW)

	#sevSeg = SevenSegThread(3, "sevSeg")
	#sevSeg.daemon = True
	#sevSeg.start()

	while exitFlag == 0:
		input_state = GPIO.input(40)
		#print(str(input_state))
		
		# when toggle goes from off to on
		if input_state == True and switchFlag == 0:
			switchFlag = 1
			counter += 1
			
			print("\nSwitch on.\n")	
			# start the hallsensor thread
			hall1 = HallThread(1, "hall1", counter, 35, 1, 22)
			hall2 = HallThread(2, "hall2", counter, 37, 2, 22)
			hall1.start()
			hall2.start()		
			time.sleep(0.5)
			
		
		# when toggle goes from on to off
		elif input_state == False and switchFlag == 1:
			switchFlag = 0
			
			print("\nSwitch off.\n")
			
			# end the hallsensor thread
			hall1.setFlag(0)
			hall2.setFlag(0)
			time.sleep(0.5)


#start()
