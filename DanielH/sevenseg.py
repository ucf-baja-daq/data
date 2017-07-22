import sharedValues

import threading
import time
import math

# flag to exit the program
exitFlag = 0

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#           e  d   dp  c   g   b   f   a
segments = (7, 21, 12, 23, 15, 18, 31, 32)
#		  1  2  3  4
digits = (33,29,22,16)

ON = 0
OFF = 1



def sevenSeg():
			#        e    d    dp   c    g    b    f    a
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

	for seg in segments:
		GPIO.setup(seg, GPIO.OUT)
		GPIO.output(seg, False)

	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)
	
	num = 1
	length = 0
	
	inputStr = str( int(num) )
	#print(inputStr)
	length = len(inputStr)
	display = [0]*length
	actualDigits = [0]*length

	for i in range (0,length):
		display[i] = inputStr[i]           # putting input Number into display array

	k = 3
	for i in range (length - 1, -1, -1):
		actualDigits[i] = digits[k]
		k = k - 1
	
	#inputStr = str( int(num) )
	while True:
		#if hallSensor1.getFlag() == 0:
		prevNum = num
		#if prevNum != 0:
			#num = activeMphValues[0]			#get the Mph value from hall sensor python file
		num = sharedValues.getSpeed()
		#print(num)
			#else:
			#	num = num
			#if( not(int(num) % 2) ):
		inputStr = str( int(num) )
			#print(inputStr)
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
			
			#print(str(onOFF_value))

			j = 0
			for val in onOFF_value:
				GPIO.output( segments[j], val )
				j = j + 1

			GPIO.output(dig, True)
			time.sleep(0.001)
			GPIO.output(dig, False)

			i = i + 1


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
		
		#global speedNumber
		
		while True:
			#if hallSensor1.getFlag() == 0:
			prevNum = self.num
			#if prevNum != 0:
			self.num = hallSensors_dan.speedNumber
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
