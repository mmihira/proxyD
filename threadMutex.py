#!/usr/bin/env python

import time
import threading
import thread
import affinity

class TObj (threading.Thread):

    def __init__(self, _name, _writeLock):
        threading.Thread.__init__(self)
        self.name = _name
        self.lock = _writeLock

    def run(self):
        while 1:
            self.lock.acquire()
            print str(threading.currentThread().ident) + ' ' + self.name + " Aquired lock"
            i = 0
            while i < 100:
                i += 1
            time.sleep(0.2)
            self.lock.release()

writeLock = thread.allocate_lock()

print str(affinity.get_process_affinity_mask(0))

t1 = TObj("First Thread", writeLock)
t2 = TObj("Second Thread", writeLock)

t1.start()
t2.start()

time.sleep(100)


        



