# Envirosave
Python module to help save of generic environment and execution information. Sometimes we run code in a complex execution environment. When something goes wrong, we want to know as much as possible about everything, to better understand what could have gone wrong for later debug.

This module helps by saving may attributes of the environment including: running processes, modules installed, users logged in, stack trace, traceback information, and more.

The Environment object will gather the data and can then be saved (internally by pickle) to be checked later offline for patterns and lateral debug.

# Gatherers
Gatherers are used to gather information from a particular place or category. They all must inherit from ```AbstractGatherer```.

They all must define a isValid() classmethod that will return True if the Gatherer should run and False otherwise. Also they must define a gather() method that gathers data and places it in it's itemDict dictionary. This function returns True if gathering completes successfully and False otherwise.

# Environment
The Environment object invokes all gathers to fill up the gatheredData dictionary.

The important functions are .gather(), .save(), and the classmethod .load()
The important instance variable is .gatheredData. This is filled after gather() is called

# Example
```
from envirosave.environment import Environment
e = Environment()
e.gather()
with open('a.bin', 'wb') as f: 
    f.write(s.save())

print (e)

# later on
with open('a.bin', 'rb') as f:
    e2 = Environment.load(f.read())

print (e2)

# To access the raw data that was saved, use <env>.gatheredData
```

# To Install
```
python setup.py install
```
