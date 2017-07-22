import sys
sys.path.insert(0, '/home/pi/ABElectronics_Python3_Libraries/ADCDifferentialPi')

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import time
import math
import RPi.GPIO as GPIO

# ADC Setup
channel = 3     # analog channel number (1-8 inclusive)
bitRate = 12    # programmable data rate 
                    # 18 (3.75 SPS) less per sec. but more accurate
                    # 16 (  15 SPS) --
                    # 14 (  60 SPS) --
                    # 12 ( 240 SPS) more per sec. but less accurate
                    
i2cAddr1 = 0x68 # these addresses are associated with the Address Config. 1
i2cAddr2 = 0x69

def StrainGauge():
	text_file = open("strainGuage_Data.txt", "w")

	i2c_helper = ABEHelpers()
	bus = i2c_helper.get_smbus()
	adc = ADCDifferentialPi(bus, i2cAddr1, i2cAddr2, bitRate)

	adc.set_pga( 1 )    # Set the gain of the PDA on the chip (Parameters: gain - 1,2,4,8)

	prev_voltage = 0
	
	for i in range( 10000 ):
		voltage = adc.read_voltage( channel )               # voltage output from strain Gauge

		changeInVoltage = voltage - prev_voltage
		prev_voltage = voltage

		#print( str(changeInVoltage * 1000) )
		
		text_file.write( str(voltage) + "\n" )
		#print( "Voltage: " + str(voltage) )
		#print( "Change: " + str(changeInVoltage) + "\n")

		#time.sleep( 0.5000 )

	#text_file.close()
	
StrainGauge()
