'''
Created on 17 Jan 2015

@author: Kristjan
'''

from time import time
_tstart_stack = []

def tic():
    _tstart_stack.append(time())

def toc(fmt="Elapsed: %.2f s"):
    print(fmt % (time() - _tstart_stack.pop()))