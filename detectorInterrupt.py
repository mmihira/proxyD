#!/usr/bin python 

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

pir = 12
GPIO.setup(pir,GPIO.IN)

print "Waiting for sensor to settle"
time.sleep(2)
print "Detecting Motion"


class CallBack:

	def __init__(self):
		self.count = 0

	def callback(self,pir):
 		self.count += 1
 		print str(self.count) + " Motion Detected"


cObj = CallBack()
cObj.callback(2)

try:
	GPIO.add_event_detect(12,GPIO.RISING,callback = cObj.callback)
	while 1:
		time.sleep(100)
	
except KeyboardInterrupt:
	print "Exiting"
	GPIO.cleanup()




