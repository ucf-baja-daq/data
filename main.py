import baja
#import hallSensor_SingleSample
import clearDisplay
import hallSensor1
import hallSensor2
import SevenSeg
import threadKiller

import sys
import _thread
import threading
import time

globalValue = 123456777

def main():

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
			clearDisplay.clear()
			sys.exit()
			
		elif inputStr == "hall" and hallSensorChk1 == False and hallSensorChk2 == False:
			hallThread1 = _thread.start_new_thread( hallSensor1.hallSen, () )
			sevSegThread = _thread.start_new_thread( SevenSeg.displayNum, (0, ) )
			hallThread2 = _thread.start_new_thread( hallSensor2.hallSen, () )
			hallSensorChk1 = True
			sevSegChk = True
			hallSensorChk2 = True
			
		elif inputStr == "hall" and ( hallSensorChk1 == True or hallSensorChk2 == True ) :
			print ("hall sensor currently running")
		
		elif inputStr == "killhall" and ( hallSensorChk1 == True or hallSensorChk2 == True ):
			SevenSeg.killSeg()
			hallSensor1.killHall()
			hallSensor2.killHall()
			clearDisplay.clear()
			_thread.exit()
		
		elif inputStr == "wipe":
			clearDisplay.clear()
			#time.sleep(10)
		
		elif inputStr == "baja" and bajaChk == False:
			bajaThread = _thread.start_new_thread( baja.Baja, () )
			bajaChk = True
		
		elif inputStr == "baja" and bajaChk == True:
			print ("baja currently running")
		
		elif inputStr == "killbaja" and bajaChk == True:
			#bajaThread.stop()
			print(str(threadKiller.getBajaKillChk()))
			threadKiller.setBajaKillChk( True )
			print(str(threadKiller.getBajaKillChk()))
			clearDisplay.clear()
			bajaChk = False
			#_thread.exit()
		
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
	
### ON RUN ###

## display help
help()

## run prompt
main()
