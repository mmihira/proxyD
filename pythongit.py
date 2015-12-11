#!/usr/bin/env python
import sys
import subprocess
from os.path import expanduser,join,splitext
from os import walk

class GitPush:

    def __init__(self):

        self.root = "~/c/proxyData/"
        self.root = expanduser(self.root)


    def push(self):

       subprocess.call(['git','-C', self.root ,'add','--all'],shell=False)
       subprocess.call(['git','-C', self.root ,'commit','-m','test'],shell=False)
       subprocess.call(['git','-C', self.root ,'push','origin','master'],shell=False)



a = GitPush()

a.push()




