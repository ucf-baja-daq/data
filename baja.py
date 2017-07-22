import time
import math
import RPi.GPIO as GPIO
import threadKiller

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

ON  = 0
OFF = 1

segments = (7,21,12,23,15,18,31,32)
digits = (33,29,22,16)

killBajaChk = False

def killBaja():
	killBajaChk = True

def Baja():

	for seg in segments:
		GPIO.setup(seg, GPIO.OUT)
		GPIO.output(seg, False)

	for dig in digits:
		GPIO.setup(dig, GPIO.OUT)
		GPIO.output(dig, False)

	#             e    d    dp   c    g    b    f    a
	baja = { 'B':[ON , ON , OFF, ON , ON , ON , ON , ON ],
		'A':[ON , OFF, OFF, ON , ON , ON , ON , ON ],
		'J':[OFF, ON , OFF, ON , OFF, ON , OFF, OFF] }

	numKeys = [' ','0','1','2','3','4','5','6','7','8','9']

	bajaKeys = [ 'B', 'A', 'J', 'A' ]

	string = "BAJA"

	integer = 5

	length = len(string)
	actualDigits = [0]*length

	while True:
		
		if( threadKiller.getBajaKillChk() ):
			break
		
		i = 0

		k = 3
		for i in range (length - 1, -1, -1):
			actualDigits[i] = digits[k]
			k = k - 1

		for dig in actualDigits:
			onOFF_value = baja[string[i]]
		
			j = 0
			for val in onOFF_value:
				GPIO.output( segments[j], val )
				j = j + 1

			GPIO.output(dig, True)
			time.sleep(0.0005)
			GPIO.output(dig, False)
	
			i = i + 1

