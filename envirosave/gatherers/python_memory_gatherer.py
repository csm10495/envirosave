'''
File: python_memory_gatherer.py - Gathers info via the mem_top module about memory usage
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import inspect
import os
import sys

from abstract_gatherer import AbstractGatherer
from mem_top import mem_top

class PythonMemoryGatherer(AbstractGatherer):
    '''
    Gathers info about our process' memory usage
    '''
    @classmethod
    def isValid(cls):
        '''
        return True if this gatherer can be run right now
            otherwise return False
        '''
        return True

    def gather(self):
        '''
        return True if it worked and itemDict is being updated,
            otherwise return False
        '''
        self.addFunctionOutput(mem_top)
        return True