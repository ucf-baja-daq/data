Alex Voce
Jay Bulsara
Daniel Healy	***

=============
hallSensor.py
=============
	ADC:
		Channel      = 1
	Pi:
		Power (3v3)  = 1
		Ground (GND) = 6

===============
strainGuages.py
===============
	ADC:
		Channel (pos&neg) = 2
		Ground (GND)      = 2
	Pi:
		Power (5v)        = 2

=================
7-Segment Display
=================
xyz & xyzMain
	Pin Diagram:

           12 11 10  9  8  7
       _____|__|__|__|__|__|_____
      |       __ __ __ __        |	*Display image is front forward.
      |      |__|__|__|__|       |	  (front of display facing out of comp. screen)
      |__________________________|	*Pins on perfboard are in same orientation 
            |  |  |  |  |  |	
            1  2  3  4  5  6

	Segments Diagram:


  	     |a|
 	 |f|     |b|
 	     |g|   
 	 |e|     |c|
 	     |d|     |DP|

	ADC:
		None.

	Pi:     Display#		
		1  - e		= 7  (GCLK)
		2  - d		= 21 (IO17)
		3  - DP		= 12 (IO18)	(decimal point) not used
		4  - c		= 23 (IO27)
		5  - g		= 15 (IO22)
		6  - digit 4	= 16 (IO23)

		7  - b		= 18 (IO24)
		8  - digit 3	= 22 (IO25)
		9  - digit 2	= 29 (IO5)
		10 - f		= 31 (IO6)
		11 - a 		= 32 (IO12)
		12 - digit 1	= 33 (IO13)


GPIO Pins:
Used Pins: ADC  [11,12,15] (16 used by digital to analog code)l
	   7seg [7,21,13,23,15,16,18,22,29,31,32,33]
	   Hall [35,37]
	   Togl [40,3,5][hall,missile,strain]
	   Led  [36,38]

Free Pins: 19,24,26 