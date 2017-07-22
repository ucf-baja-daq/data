#toggleThreadTest.py

import threading
import time

# flag to exit the program
exitFlag = 0

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # sets up a pull up resistor

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
		self.counter = counter
		self.pinNumber = pinNumber
		self.hallSensor_Num = hallSensor_Num
		self.diameter = diameter
		
		# toggle switch flag
		self.runningFlag = 1
		
		# setup input pin for hallsensor
		GPIO.setup( pinNumber, GPIO.IN )
		
		# open file to write to
		# based on pin number and counter
		self.text_file = open("data/hallSen_Data"+ str(pinNumber) + "_" + str(counter) + ".txt", "w")
		
		# initial time for time vector
		self.initTime = time.time()
		
		# initialize 
		self.t1 = 0
		self.t2 = 0
		self.hallFlag = 0
		self.gearRatio = 11.5
		
		print("Done.\n")
		
		
		
	def run(self):
		print("Running hall sensor on pin " + str(self.pinNumber) + ".")
		# while switch is toggled on
		while self.runningFlag == 1:
			self.input_hallSen = GPIO.input( self.pinNumber )
			self.curTime = time.time() - self.initTime
			
			if self.input_hallSen == 1 and self.hallFlag == 0:
				self.hallFlag = 1
				self.t1 = self.t2													# stores the previous current time from curTime
				self.t2 = self.curTime											# stores the current time in curTime
				self.rpm = 60/(self.t2 - self.t1)
				
				print(self.name + str(self.curTime) + "," + str(self.rpm))
				self.text_file.write( str(self.curTime) + "," + str(self.rpm) + "\n" )
				self.text_file.flush()
			elif self.input_hallSen == 1 and self.hallFlag == 1:
				self.filler = 0
			
			else:
				self.hallFlag = 0
		self.text_file.close()
	
	def setFlag(self, flag):
		self.runningFlag = flag
		

counter = 0
switchFlag = 0

while exitFlag == 0:
	input_state = GPIO.input(7)
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
	
		
	



