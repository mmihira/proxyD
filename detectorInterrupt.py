#!/usr/bin python 

import RPi.GPIO as GPIO
import time
import thread
import threading
import subprocess
from os.path import expanduser,join,splitext

GPIO.setmode(GPIO.BOARD)

# The proximity detector is installed
# on port 12
pir = 12

GPIO.setup(pir,GPIO.IN)

print "Waiting for sensor to settle"
time.sleep(2)
print "Detecting Motion"


class GitPush:

    def __init__(self):

        self.root = "~/proxyData/"
        self.root = expanduser(self.root)


    def push(self):

       subprocess.call(['git','-C', self.root ,'add','--all'],shell=False)
       subprocess.call(['git','-C', self.root ,'commit','-m',time.strftime('%Y-%m-%d %H:%M:%S')],shell=False)
       subprocess.call(['git','-C', self.root ,'push','origin','master'],shell=False)




"""
logWriter is a asychronous file writer
which logs all detected movement to a 
text file. Also it will push these changes
to a specified remote directory

A thread.lock object is passed in as
argument which each thread that references
this writer will acquire before writing
"""
class logWriter:

    def __init__(self,_lock):
        self.log = open('/home/pi/proxyData/data.txt','w')
        self.log.write('-- Starting log\n')
        self.lock = _lock
	self.gitWriter = GitPush()

    def writeLnToLog(self, msg):
        self.lock.acquire()
        self.log.write(msg + '\n')
        self.log.flush()
	self.gitWriter.push()
        self.lock.release()


class CallBack:

	def __init__(self,_log):
		self.count = 0
                self.log = _log

	def callback(self,pir):
 		self.count += 1
 		print str(self.count) + " Motion Detected"
                self.log.writeLnToLog(time.strftime('%Y-%m-%d %H:%M:%S') + ', - Detected - Count : ,' + str(self.count))

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








