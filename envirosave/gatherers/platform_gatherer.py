'''
File: platform_gatherer.py - Gathers info via the platform module
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import inspect
import os
import platform
import subprocess

from abstract_gatherer import AbstractGatherer

class PlatformGatherer(AbstractGatherer):
    '''
    Gathers info from the platform module
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
        # Get everything from platform
        for name in dir(platform):
            obj = getattr(platform, name)
            if callable(obj) and not name.startswith('_'):
                self.addFunctionOutput(obj, hideException=True)
        
        return True