#!/usr/bin python 

import RPi.GPIO as GPIO
import time
import thread
import threading

GPIO.setmode(GPIO.BOARD)

pir = 12
GPIO.setup(pir,GPIO.IN)

print "Waiting for sensor to settle"
time.sleep(2)
print "Detecting Motion"

class logWriter:

    def __init__(self,_lock):
        self.log = open('log.txt','w')
        self.log.write('-- Starting log\n')
        self.lock = _lock

    def writeLnToLog(self, msg):
        self.lock.acquire()
        self.log.write(msg + '\n')
        self.log.flush()
        self.lock.release()


class CallBack:

	def __init__(self,_log):
		self.count = 0
                self.log = _log

	def callback(self,pir):
 		self.count += 1
 		print str(self.count) + " Motion Detected"
                self.log.writeLnToLog(time.strftime('%Y-%m-%d %H:%M:%S') + ' - Detected - Count : ' + str(self.count))

# The main write lock
writeLock = thread.allocate_lock()

# Create the log file
log =  logWriter(writeLock)

# The main function
cObj = CallBack(log)

time.sleep(0.5)


try:
	GPIO.add_event_detect(12,GPIO.RISING,callback = cObj.callback)
	while 1:
		time.sleep(100)
	
except KeyboardInterrupt:
	print "Exiting"
	GPIO.cleanup()




