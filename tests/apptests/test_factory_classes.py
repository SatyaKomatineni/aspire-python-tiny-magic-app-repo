"""
*************************************************
* classes to be used for testing factory instantiation
*************************************************
About:
1. Used in conjunction with test_factory_x.py

"""
from src.aspire_tinyapp.interfaces.objectinterfaces import (
    ISingleton, 
    IInitializable, 
    IInitializableWithArgs,
    IExecutor)

from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.publicinterfaces import factory

"""
*************************************************
* Test1, class1: TestSingletonClassNoConstructor
*************************************************
about:
1. No constructor
2. Singleton

config entry:
[testclasses_class1]
classname="apptests.test_factory_classes.TestSingletonClassNoConstructor"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class1", None)
"""

class TestSingletonClassNoConstructor(ISingleton):
    def __init__(self):
        self.name = "TestSingletonClass"
        log.info("TestSingletonClassNoConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test1():
    obj = factory.getObjectAbsolute("testclasses_class1", None)
    log.prettyPrintObject(obj)

"""
*************************************************
* Test2, class21: TestSingletonClassWithConstructor
*************************************************
about:
1. Constructor with 2 args
2. Singleton

config entry:
[testclasses_class2]
classname="apptests.test_factory_classes.TestSingletonClassWithConstructor"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class1", None)
"""

class TestSingletonClassWithConstructor(ISingleton):
    def __init__(self, param1: str, param2: str):
        self.param1 = param1
        self.param2 = param2
        log.info("TestSingletonClassWithConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test2():
    obj = factory.getObjectAbsolute("testclasses_class2", None)
    log.prettyPrintObject(obj)
