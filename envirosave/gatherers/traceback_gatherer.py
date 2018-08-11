'''
File: traceback_gatherer.py - Gathers information about the last traceback
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import inspect
import os
import traceback
import sys

from abstract_gatherer import AbstractGatherer

class TracebackGatherer(AbstractGatherer):
    '''
    Gathers information about the current traceback
    '''
    @classmethod
    def isValid(cls):
        '''
        return True if this gatherer can be run right now
            otherwise return False
        '''
        # Check if there was ever an exception passed
        return getattr(sys, 'last_type', None) is not None

    def gather(self):
        '''
        return True if it worked and itemDict is being updated,
            otherwise return False
        '''
        # Mark if this exception is being handled
        self.itemDict['IsBeingHandled'] = sys.exc_info()[0] is not None
        if sys.last_type:
            self.itemDict['TracebackPrintout'] = ''.join(traceback.format_exception(sys.last_type, sys.last_value, sys.last_traceback))

        return True