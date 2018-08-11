'''
File: stack_gatherer.py - Gathers info from the python stack
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import inspect
import os
import sys

from collections import namedtuple

from six import iteritems
from six.moves import cPickle as pickle
from six.moves import builtins

from abstract_gatherer import AbstractGatherer

PickleableStackFrame = namedtuple('PickleableStackFrame', ['Locals', 'Globals', 'FrameInfo'])

class StackGatherer(AbstractGatherer):
    '''
    Gathers info from the Python stack
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
        stack = inspect.stack()
        buildList = []
        for itm in stack:
            frame = itm[0]
            psf = PickleableStackFrame(self._toPickleableDict(frame.f_locals), self._toPickleableDict(frame.f_globals), inspect.getframeinfo(frame))
            buildList.append(psf)

        self.itemDict['StackFrameList']  = buildList
        return True

    @classmethod
    def _canPickle(cls, obj):
        '''
        returns True if this item can be pickled, otherwise False
        '''
        try:
            pickle.dumps(obj, -1)
            return True
        except Exception as ex:
            return False

    @classmethod
    def _toPickleableDict(cls, d):
        '''
        Takes a dictionary of name->object and returns a version of it that
            can be pickled. (If it can't be pickled it is removed from the return dict)
        '''
        retDict = {}
        for key, value in iteritems(d):
            if not key.endswith('__') and cls._canPickle(value):
                retDict[key] = value
        return retDict
