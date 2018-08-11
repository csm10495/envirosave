'''
File: abstract_gatherer.py
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import datetime
import os
import pprint
import threading
import time
import subprocess
GATHERER_MAGIC = 'Gatherer Magic!' # set on all gatherers to know they are gatherers

from six import iteritems, string_types

class AbstractGatherer(object):
    '''
    abstract class for all gatherers to extend from
    '''
    MAGIC = GATHERER_MAGIC
    def __init__(self):
        '''
        initializer. Also sets up the itemDict and a lock on it for async access
        '''
        self.itemDict = {}
        self.threads = []
        self.itemDictLock = threading.Lock()

    def __getstate__(self):
        '''
        used for pickling
        '''
        d = self.__dict__
        d['itemDictLock'] = None
        return d

    def __setstate__(self, d):
        '''
        used for pickling
        '''
        self.__dict__ = d
        self.itemDictLock = threading.Lock()

    def __getattribute__(self, name):
        '''
        this is used as a hack to ensure we get a start/end time for all gatherers
            it also will force a wait until all threads are complete before returning 
                from the call to gather()
        '''
        if name == 'gather':
            def gatherWrapper(*args, **kwargs):
                self.itemDict['StartTime'] = datetime.datetime.now()
                if object.__getattribute__(self, name)(*args, **kwargs):
                    self._waitTillGatheringIsComplete()
                    self.itemDict['EndTime'] = datetime.datetime.now()
                    return True
                return False
            return gatherWrapper

        return object.__getattribute__(self, name)

    def parse(self, outFile=None):
        '''
        utility function to parse the data to screen or file
        '''
        s = str(self)
        if outFile:
            with open(outFile, 'a+') as f:
                f.write(s)
        else:
            print (s)

    def parseToFolder(self, outDir):
        '''
        utility to turn itemDict into a folder of files per entry
        '''
        try:
            os.makedirs(outDir)
        except:
            pass
        
        for key, value in iteritems(self.itemDict):
            outFile = os.path.join(outDir, key.replace("/", "_").replace("\\", "_").replace(":", '_').replace("\"", "_").replace("*", "_"))
            if hasattr(value, 'toEnvirosaveBinary'):
                # Maybe we should save binary instead of text?
                value.toEnvirosaveBinary(outFile)
            else:
                with open(outFile, 'w') as f:
                    if isinstance(value, string_types):
                        f.write(value)
                    else:
                        f.write(pprint.pformat(value, width=200))

    def __str__(self):
        '''
        returns a string representation of the gatherer (via its itemDict)
        '''
        retStr = ''
        for key, value in self.itemDict.items():
            retStr += '%-20s : \n  %s\n' % (key, str(value).replace('\n', '\n  ').rstrip(' '))

        return retStr

    def addShellOutput(self, cmd):
        '''
        Will call a thread to do the shell call
        '''
        t = threading.Thread(target=self._addShellOutput, args=(cmd,))
        t.start()
        self.threads.append(t)

    def _addShellOutput(self, cmd):
        '''
        Calls the cmd in a subprocess to put the output in the itemDict
        '''
        try:
            tmp = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError:
            return # fail?

        with self.itemDictLock:
            self.itemDict[cmd] = tmp

    def addFunctionOutput(self, func, args=None, nameOverride=None, hideException=False):
        '''
        runs a function in a thread and saves the return data in the itemDict
        '''
        t = threading.Thread(target=self._addFunctionOutput, args=(func, args, nameOverride, hideException))
        t.start()
        self.threads.append(t)

    def _addFunctionOutput(self, func, args=None, nameOverride=None, hideException=False):
        '''
        called by addFunctionOutput() in a thread
        '''
        if args is None:
            args = []

        name = nameOverride or func.__name__
        try:
            result = func(*args)
        except:
            if not hideException:
                raise
            else:
                return

        with self.itemDictLock:
            self.itemDict[name] = result

    def _waitTillGatheringIsComplete(self, timeout=10):
        '''
        Called to complete gathering
        '''
        deathTime = time.time() + timeout
        while time.time() < deathTime:
            numAlive = 0
            for i in self.threads:
                i.join(.0001)
                if i.isAlive():
                    numAlive += 1

            if numAlive == 0:
                self.threads = []
                break

            time.sleep(.0001)
        else:
            raise RuntimeError("Timeout waiting for gathering to complete!")

    @classmethod
    def isValid(cls):
        '''
        return True if this gatherer can be run right now
            otherwise return False
        '''
        raise NotImplementedError

    def gather(self):
        '''
        return True if it worked and itemDict is being updated,
            otherwise return False
        '''
        raise NotImplementedError