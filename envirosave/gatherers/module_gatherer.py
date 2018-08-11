'''
File: module_gatherer.py - Gathers all pip modules
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import inspect
import os
import sys

from abstract_gatherer import AbstractGatherer

class ModuleGatherer(AbstractGatherer):
    '''
    Gathers all installed python modules
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
        self.addShellOutput('\"%s\" -m pip freeze' % sys.executable)
        return True