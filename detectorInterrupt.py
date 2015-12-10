#!/usr/bin python 

import RPi.GPIO as GPIO
import time
import thread
import threading

GPIO.setmode(GPIO.BOARD)

# The proximity detector is installed
# on port 12
pir = 12

GPIO.setup(pir,GPIO.IN)

print "Waiting for sensor to settle"
time.sleep(2)
print "Detecting Motion"

"""
logWriter is a asychronous file writer
which logs all detected movement to a 
text file

A thread.lock object is passed in as
argument which each thread that references
this writer will acquire before writing
"""
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

# Need to use global variables because add_event_detect doesn't work well
# with object methods as callbacks
count = 0

# The main write lock
writeLock = thread.allocate_lock()

# Create the log file
log =  logWriter(writeLock)

# The main function
cObj = CallBack(log)

runProgram = 1
while runProgram :

	try:
		GPIO.add_event_detect(12,GPIO.RISING,callback = cObj.callback)
		print "Edge detection added successfully"

		while 1:
			time.sleep(100)
		
	except KeyboardInterrupt:
		print "Exiting"
		GPIO.cleanup()
		runProgram = 0

	except RuntimeError, e:

		if e.message == 'Failed to add edge detection' :
			print e.message
			print "Retrying"
		else:
			print 'Exiting for unknown error : ' + e.message
			GPIO.cleanup()
			runProgram = 0








