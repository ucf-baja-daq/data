import _thread
import time
import math

import sys
sys.path.insert(0, '/home/pi/ABElectronics_Python3_Libraries/ADCDifferentialPi')

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#Global Variables
################# baja
ON = 0
OFF = 1
segments = (7,11,12,13,15,18,31,32)
digits = (33,29,22,16)
bajaThreadActive = False

################# hallsensor1
activeHallSensors = []		#boolean values that keep a hallsensor ON/OFF
activeMphValues = []

################# sevenSeg
sevenSegActive = False
mph = 0


def main(hallSensor1Diameter, hallSensor2Diameter ):
	global bajaThreadActive
	global hallSensor1Active
	global hallSensor2Active
	global sevenSegActive

	## Boolean check values
	## used to check whether that process is already running
	bajaChk = False
	hallSensorChk1 = False
	hallSensorChk2 = False
	sevSegChk = False
	
	## initialize thread names
	bajaThread = None
	hallThread1 = None
	hallThread2 = None
	sevSegThread = None

	#threadKillerThread = _thread.start_new_thread( threadKiller.init, () )

	while True:

		## prompt
		inputStr = input(">> ")
		
		## command tree
		if inputStr  == "help":
			help()

		elif inputStr  == "quit" or inputStr  == "exit":
			clearDisplay()
			sys.exit()
			
		elif inputStr == "hall" and hallSensorChk1 == False and hallSensorChk2 == False:
			# input values for hallSen: hallSensor_Num, adcChannel_Num, adcBitRate_Num, i2cAddr1_Num, i2cAddr2_Num, outputFile_Name, diameter_Num, hallSensorActive
			#hallThread1 = _thread.start_new_thread( hallSen, (1, 1, 12, 0x68, 0x69, "hallSensor_Data_1.txt", hallSensor1Diameter, True) )
			#sevSegThread = _thread.start_new_thread( SevenSeg.displayNum, (0, ) )
			#hallThread2 = _thread.start_new_thread( hallSen, (2, 2, 12, 0x68, 0x69, "hallSensor_Data_2.txt", hallSensor2Diameter, True) )
			
			#digital hallsensor threads
			#hallThread1 = _thread.start_new_thread( hallSenDigital, (35, 1, hallSensor1Diameter, True) )
			hallThread1 = _thread.start_new_thread( hallSenDigital35, (1, hallSensor1Diameter, True) )
			print("hallsensor1 started");
			
			time.sleep(3)
			
			sevenSegActive = True
			sevSegThread = _thread.start_new_thread( sevenSeg, () )
			
			time.sleep(3)
			#hallThread2 = _thread.start_new_thread( hallSenDigital, (37, 2, hallSensor2Diameter, True) )
			hallThread2 = _thread.start_new_thread( hallSenDigital37, (2, hallSensor2Diameter, True) )
			print("hallsensor2 started");
			
			hallSensorChk1 = True
			sevSegChk = True
			hallSensorChk2 = True
			
		elif inputStr == "hall" and ( hallSensorChk1 == True or hallSensorChk2 == True ) :
			print ("hall sensor currently running")
		
		elif inputStr == "killhall" and ( hallSensorChk1 == True or hallSensorChk2 == True ):
			#SevenSeg.killSeg()
			activeHallSensors[0] = False
			print("hallsensor1 terminated");
			
			sevenSegActive = False
			
			activeHallSensors[1] = False
			print("hallsensor2 terminated");
			
			hallSensorChk1 = False
			sevSegChk = False
			hallSensorChk2 = False
			clearDisplay()
			#_thread.exit()
		
		elif inputStr == "wipe":
			clearDisplay.clear()
			#time.sleep(10)
		
		elif inputStr == "baja" and bajaThreadActive == False:
			bajaThread = _thread.start_new_thread( baja, () )
			bajaThreadActive = True
		
		elif inputStr == "baja" and bajaThreadActive == True:
			print ("baja currently running")
		
		elif inputStr == "killbaja" and bajaThreadActive == True:
			bajaThreadActive = False
			clearDisplay()
		
		else:	## on unknown command
			print ("you done goofed, Wyatt") ## Wyatt - Team Lead Fall 2016
			
			

def help():		## displays list of available commands
	print ("Commands:")
	print ("\t>> hall")
	print ("\t>> killhall")
	print ("\t>> wipe (to clear the 7seg display)")
	print ("\t>> baja")
	print ("\t>> killbaja\n")

	print ("Exit Main.py:")
	print ("\t>> quit\n\t>> exit\n")
	
def clearDisplay():
	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)	

def baja():
	global segments
	global digits
	
	for seg in segments:
		GPIO.setup(seg, GPIO.OUT)
		GPIO.output(seg, False)
		
	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)
		
	#             e    d    dp   c    g    b    f    a
	BAJA = { 'B':[ON , ON , OFF, ON , ON , ON , ON , ON ],
			 'A':[ON , OFF, OFF, ON , ON , ON , ON , ON ],
			 'J':[OFF, ON , OFF, ON , OFF, ON , OFF, OFF] }
			 
	numKeys = [' ','0','1','2','3','4','5','6','7','8','9']
	bajaKeys = ['B','A','J','A']
	string = "BAJA"
	
	length = len(string)
	actualDigits = [0]*length
	
	while bajaThreadActive:
		i = 0
		k = 3
		
		for i in range(length - 1, -1, -1):
			actualDigits[i] = digits[k]
			k = k - 1
		
		for dig in actualDigits:
			onOFF_value = BAJA[string[i]]
			
			j = 0
			for val in onOFF_value:
				GPIO.output( segments[j], val )
				j = j + 1
				
			GPIO.output(dig, True)
			time.sleep(0.0005)
			GPIO.output(dig, False)	
	
			i = i + 1
	
def getMph():
	global mph
	return mph
	
def hallSen(hallSensor_Num, adcChannel_Num, adcBitRate_Num, i2cAddr1_Num, i2cAddr2_Num, outputFile_Name, diameter_Num, hallSensorActive):
	# ADC Setup
	channel = 1		# analog channel number (1-8 inclusive)
	bitRate = 12	# programmable data rate
					# 18 (3.75 SPS) less per sec. but more
					# 16 (  15 SPS) --
					# 14 (	60 SPS) --
					# 12 ( 240 SPS) more per sec. but less accurate
	
	i2cAddr1 = 0x68 # these address are associated with the Address Config. 1
	i2cAddr2 = 0x69
	
	text_file = open("hallSensor_Data1.txt", "w")
	initTime = time.time()
	
	t1 = 0
	t2 = 0
	
	flag = 0
	diameter = 14	# need to find the actual diameter !!!
	
	i2c_helper = ABEHelpers()
	bus = i2c_helper.get_smbus()
	adc = ADCDifferentialPi(bus, i2cAddr1, i2cAddr2, bitRate)
	
	global activeMphValues
	global flagThread
	
	global activeHallSensors
	activeHallSensors.append(hallSensorActive)
	
	mph = 0
	activeMphValues.append(mph)
	#activeMphValues[hallSensor_Num-1] = mph
	
	while activeHallSensors[hallSensor_Num-1]:
		voltage = adc.read_voltage( channel )					# voltage output from hall sensor (either a pos. or neg. value)
		curTime = time.time() - initTime						# calculates the current time from time acc. minus time started with
			
		if voltage < 0.0 and flag == 0:							# if voltage is neg. and we have not passed by the magnet yet
			flag = 1
			t1 = t2													# stores the previous current time from curTime
			t2 = curTime											# stores the current time in curTime
			rps = 1/(t2 - t1)										# revolutions per second
			activeMphValues[hallSensor_Num-1] = (rps * (math.pi) * diameter * (3600/63360)) / 11.5			# conversion from rps to miles per second
			#temp = rps * (math.pi) * diameter * (3600/63360)
			rpm = rps * 60
			#activeMphValues[hallsensor_Num-1] = rpm
			#mph = rps*60
			
			#print( str(curTime + "," + str(voltage) + "," + str(mph) )
			text_file.write( str(curTime) + "," + str(rpm)  + "\n" )
			text_file.flush()
				
		elif voltage < 0.0 and flag == 1:						# else if voltage is neg. but we are currently still passing by the magnet
			#print( str(curTime) + "," + str(voltage) )
			#text_file.write( str(curTime) + "," str(voltage) + "\n" )
			filler = 0
				
		else:													# else the voltage is positive (meaning the magnet is not next to the hall sensor)
			flag = 0
			#print( str(curTime) + "," + str(voltage) )
			#text_file.write( str(curTime) + "," + str(voltage) + "\n" )
			flag = 0		# added hopefully no problems, if problems comment this out
				
		#time.sleep( 0.0100 )
			
	text_file.close()

def hallSenDigital(pinNumber, hallSensor_Num, diameter_Num, hallSensorActive):
	GPIO.setup( pinNumber, GPIO.IN )

	text_file = open("hallSen_Data"+str(pinNumber)+".txt", "a")
	initTime = time.time()
	#print (str(initTime))
	text_file.write("start")
	text_file.flush()

	t1 = 0
	t2 = 0
	flag = 0
	diameter = diameter_Num
	gearRatio = 11.5
	
	global activeMphValues
	global flagThread
	
	global activeHallSensors
	activeHallSensors.append(hallSensorActive)
	
	mph = 0
	activeMphValues.append(mph)

	while activeHallSensors[hallSensor_Num-1]:
		input_hallSen = GPIO.input( pinNumber )
		curTime = time.time() - initTime

		if input_hallSen == 1 and flag == 0:
			flag = 1
			t1 = t2													# stores the previous current time from curTime
			t2 = curTime											# stores the current time in curTime
			rps = 1/(t2 - t1)										# revolutions per second
			
			activeMphValues[hallSensor_Num-1] = (rps * (math.pi) * diameter * (3600/63360)) / gearRatio			# conversion from rps to miles per second
			
			rpm = rps*60
			#activeMphValues[hallSensor_Num-1] = rpm
			
			#mph = rps*60
			#print( str(curTime + "," + str(voltage) + "," + str(mph) ) )
			#print(str(input_hallSen) + ", " + str(activeMphValues[hallSensor_Num-1]))
			text_file.write( str(curTime) + "," + str(rpm) + "," + str(activeMphValues[hallSensor_Num-1]) + "\n" )
			text_file.flush()

		elif input_hallSen == 1 and flag == 1:
			
			#print( str(curTime) + "," + str(voltage) )
			#text_file.write( str(curTime) + "," str(voltage) + "\n" )
			filler = 0
			
		else:
			
			#print( str(curTime) + "," + str(voltage) )
			#text_file.write( str(curTime) + "," + str(voltage) + "\n" )
			flag = 0

		#time.sleep( 0.0500 )

	text_file.close()
	GPIO.cleanup()

def sevenSeg():
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

	global sevenSegActive
	global activeMphValues

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
	while sevenSegActive:
		#if hallSensor1.getFlag() == 0:
		prevNum = num
		if prevNum != 0:
			#num = activeMphValues[0]			#get the Mph value from hall sensor python file
			num=1
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

			j = 0
			for val in onOFF_value:
				GPIO.output( segments[j], val )
				j = j + 1

			GPIO.output(dig, True)
			time.sleep(0.0005)
			GPIO.output(dig, False)

			i = i + 1
		
			
			
				




	
### ON RUN ###

## display help
help()

## run prompt
#main(23, 23)


# input values for hallSen: hallSensor_Num, adcChannel_Num, adcBitRate_Num, i2cAddr1_Num, i2cAddr2_Num, outputFile_Name, diameter_Num, hallSensorActive
#hallThread1 = _thread.start_new_thread( hallSen, (1, 1, 12, 0x68, 0x69, "hallSensor_Data_1.txt", hallSensor1Diameter, True) )
#sevSegThread = _thread.start_new_thread( SevenSeg.displayNum, (0, ) )
#hallThread2 = _thread.start_new_thread( hallSen, (2, 2, 12, 0x68, 0x69, "hallSensor_Data_2.txt", hallSensor2Diameter, True) )

#digital hallsensor threads
#hallThread1 = _thread.start_new_thread( hallSenDigital, (35, 1, hallSensor1Diameter, True) )
hallThread1 = _thread.start_new_thread( hallSenDigital35, (1, 23, True) )
print("hallsensor1 started");

time.sleep(3)

sevenSegActive = True
sevSegThread = _thread.start_new_thread( sevenSeg, () )

time.sleep(3)
#hallThread2 = _thread.start_new_thread( hallSenDigital, (37, 2, hallSensor2Diameter, True) )
hallThread2 = _thread.start_new_thread( hallSenDigital37, (2, 23, True) )
print("hallsensor2 started");

hallSensorChk1 = True
sevSegChk = True
hallSensorChk2 = True
