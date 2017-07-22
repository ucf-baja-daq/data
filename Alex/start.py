import _thread
import hallSensors_dan
import sevenseg
#import threading

print("start")
inputLet = ""

hallChk = False

print("while")
while inputLet != "q":
	if hallChk == False:
		hallChk = True
		hallThread1 = _thread.start_new_thread( hallSensors_dan.start, () )
		sevensegthread = _thread.start_new_thread( sevenseg.sevenSeg, () )
		
	inputLet = input("type 'q' at any point and hit enter to quit: ")


_thread.exit()
