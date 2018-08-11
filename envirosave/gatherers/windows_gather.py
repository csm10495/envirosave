'''
File: windows_gather.py - Gathers info specific to Windows
Project: Envirosave: A simple attempt at saving a lot of
  information about the execution environment at a given point
Author: csm10495
Copyright: MIT License - 2018
'''
import os
import subprocess

from win32file import QueryDosDevice
from abstract_gatherer import AbstractGatherer

class WindowsGatherer(AbstractGatherer):
    '''
    Gathers info specific to Windows
    '''
    @classmethod
    def isValid(cls):
        '''
        return True if this gatherer can be run right now
            otherwise return False
        '''
        return os.name == 'nt'

    def gather(self):
        '''
        return True if it worked and itemDict is being updated,
            otherwise return False
        '''
        # Save all enumerated dos devices
        self.itemDict['DosDevices'] = ['\\\\.\\' + i for i in QueryDosDevice(None).split('\x00') if len(i)]
        
        # Save active RDP sessions
        self.addShellOutput(r'C:\Windows\System32\qwinsta.exe')

        # Add Windows systeminfo
        self.addShellOutput('systeminfo')

        # Add service info
        self.addShellOutput('sc queryex type=service state=all')

        # Add driver info
        self.addShellOutput('sc queryex type=driver state=all')

        # Add current drives
        self.addShellOutput("wmic diskdrive get * /format:list")
        self.addShellOutput("wmic logicaldisk get * /format:list")
        self.addShellOutput("wmic scsicontroller get * /format:list")

        # Add baseboard info
        self.addShellOutput("wmic baseboard get * /format:list")

        # Add bios info
        self.addShellOutput("wmic bios get * /format:list")

        # Add RAM info
        self.addShellOutput("wmic memorychip get * /format:list")

        # Get OS info
        self.addShellOutput("wmic os get * /format:list")

        return True