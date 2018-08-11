'''
File: screenshot_gatherer.py - Gathers a screenshot of system
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import mss
import mss.screenshot

from abstract_gatherer import AbstractGatherer

class EnvirosaveScreenshot(mss.screenshot.ScreenShot):
    '''
    subclass of ScreenShot to add toEnvirosaveBinary function
    '''
    def toEnvirosaveBinary(self, f):
        '''
        saves this screenshot as a png file
        '''
        mss.tools.to_png(self.rgb, self.size, output=f + ".png")

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
            # if saving files... save this as a picture!
        with mss.mss() as sct: 
            sct.cls_image = EnvirosaveScreenshot
            screenshot = sct.grab(sct.monitors[0])
            self.itemDict['Screenshot'] = screenshot

        return True
