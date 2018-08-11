'''
File: psutil_gatherer.py - Gathers info via the psutil module
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import psutil

from abstract_gatherer import AbstractGatherer

class PsutilGatherer(AbstractGatherer):
    '''
    Gathers info via psutil
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
        self.addFunctionOutput(lambda: list(psutil.process_iter()), nameOverride='Processes')
        self.addFunctionOutput(lambda: psutil.disk_io_counters(perdisk=True), nameOverride='DiskIoCounters')
        self.addFunctionOutput(lambda: psutil.users(), nameOverride='Users')

        partitions = psutil.disk_partitions()
        self.itemDict['Partitions'] = partitions

        diskUsage = {}
        # get partition usage
        for p in partitions:
            try:
                diskUsage[p.mountpoint] =  psutil.disk_usage(p.mountpoint)
            except Exception:
                pass

        self.itemDict['DiskUsage'] = diskUsage
        return True