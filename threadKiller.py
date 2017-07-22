import baja

bajaKillChk = False

def setBajaKillChk(chk):	# chk has to be a boolean value
	bajaKillChk = chk

def getBajaKillChk():
	global bajaKillChk
	return bajaKillChk

def init():
	while True:
		x = 1
