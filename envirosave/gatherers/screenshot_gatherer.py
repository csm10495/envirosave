'''
File: screenshot_gatherer.py - Gathers a screenshot of system
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import mss

from abstract_gatherer import AbstractGatherer

class ScreenshotGatherer(AbstractGatherer):
    '''
    Uses mss to take a screenshot of all monitors
    '''
    @classmethod
    def isValid(cls):
        '''
        return True if this gatherer can be run right now
            otherwise return False
        '''
        # make sure we have a monitor
        with mss.mss() as sct: 
            return len(sct.monitors) > 0

    def gather(self):
        '''
        return True if it worked and itemDict is being updated,
            otherwise return False
        '''
        with mss.mss() as sct: 
            self.itemDict['Screenshot'] = sct.grab(sct.monitors[-1])

        return True