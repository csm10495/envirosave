'''
File: environment.py - Holds the Environment object
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import importlib
import inspect
import os
import pprint
import sys
import time
import zlib

from six import iteritems
from six.moves import cPickle as pickle

from gatherers.abstract_gatherer import AbstractGatherer, GATHERER_MAGIC

THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
GATHERERS_FOLDER = os.path.join(THIS_FOLDER, 'gatherers')

class Environment(object):
    '''
    Contains the Gatherers and can execute them to fill the gatheredData dictionary with data
    '''
    def __init__(self, additionalGatherers=None):
        '''
        Initializer. Finds valid Gatherers in the gatherers folder
        '''
        self.additionalGatherers = additionalGatherers if additionalGatherers is not None else []
        self.gatherers = self._getAllValidGatherers()
        self.gatheredData = {}

    def __str__(self):
        '''
        Gets a pretty-ish string of the gatheredData
        '''
        retStr = ''
        for key, value in self.gatheredData.items():
            retStr += '%-20s : \n  %s\n' % (key, pprint.pformat(str(value), width=200).replace('\n', '\n  ').rstrip(' '))

        return retStr

    def parse(self, outFile=None):
        '''
        Helper to parse to a file or screen
        '''
        s = str(self)
        if outFile:
            with open(outFile, 'w') as f:
                f.write(s)
        else:
            print (s)

    def parseToFolder(self, outDir):
        '''
        utility to turn gatheredData into a folder of files per entry
        '''
        try:
            os.makedirs(outDir)
        except:
            pass
        
        for key, value in iteritems(self.gatheredData):
            subDir = os.path.join(outDir, key)
            value.parseToFolder(subDir)

    def _getAllValidGatherers(self):
        '''
        Finds all Gatherers in the gatherers folder.
            Returns a list of types.
        '''
        gathers = []
        names = []
        heldPath = sys.path[:] # set it back later
        try:
            sys.path.insert(1, GATHERERS_FOLDER)
            for file in os.listdir(GATHERERS_FOLDER):
                if os.path.isfile(os.path.join(GATHERERS_FOLDER, file)):
                    # remove extension
                    file = '.'.join(file.split('.')[:-1])
                    mod = importlib.import_module(file)

                for thing in dir(mod):
                    thingObj = getattr(mod, thing)
                    if thing != 'AbstractGatherer' and inspect.isclass(thingObj) and \
                     getattr(thingObj, 'MAGIC', '') == GATHERER_MAGIC and thing not in names and \
                     thingObj.isValid():
                        gathers.append(thingObj)
                        names.append(thing) # don't duplicate (it happens since we have py and pycs)
        finally:
            sys.path = heldPath

        return gathers

    def gather(self):
        '''
        Has all Gatherers gather. Returns the result dict and places it in .gatheredData
        '''
        ret = {}
        everything = self.gatherers + self.additionalGatherers
        for i in everything:
            inst = i()
            if inst.gather():
                assert len(inst.threads) == 0, "Gatherer (%s) did not complete spawned threads!" % type(inst)
                #ret[i.__name__] = inst.itemDict
                ret[i.__name__] = inst # save the gatherer

        self.gatheredData = ret
        return ret

    def save(self):
        '''
        Saves a compressed binary of the data
        '''
        p = pickle.dumps(self, -1)
        com = zlib.compress(p, 9)
        return com

    @classmethod
    def load(cls, data):
        '''
        Loads the compressed binary data into an Environment object
        '''
        p = zlib.decompress(data)
        return pickle.loads(p)

if __name__ == '__main__':
    
    start = time.time()
    e = Environment()
    end = time.time()
    print ("Time to create Environment:          %.5f seconds" % (end - start))

    start = time.time()
    g = e.gather()
    end = time.time()
    print ("Time to gather():                    %.5f seconds" % (end - start))
 
    start = time.time()
    p = e.save()
    end = time.time()
    print ("Time to pickle the gathered info():  %.5f seconds" % (end - start))

    d = e.save()
    e2 = Environment.load(d)
    