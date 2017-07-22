import RPi.GPIO as GPIO
import time
import hallSensor1

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

ON  = 0
OFF = 1

#segments = (32,31,18,15,13,11,7,12)
segments = (7,11,12,13,15,18,31,32)
digits = (33,29,22,16)

#GPIO.output(29, False)

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

def initDisplay():
	for seg in segments:
		GPIO.setup(seg, GPIO.OUT)
		GPIO.output(seg, False)

	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)

killS = False

def killSeg():
	global killS
	killS = True
	
def displayNum(num):
	global killS
	initDisplay()
	length = 0
	inputStr = str( int(num) )
	while True:
		if killS == True:
			time.sleep(10)
		else:
			if hallSensor1.getFlag() == 0:
				num = hallSensor1.getMph()			#get the Mph value from hall sensor python file
			#else:
			#	num = num
			#if( not(int(num) % 2) ):
			inputStr = str( int(num) )
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
