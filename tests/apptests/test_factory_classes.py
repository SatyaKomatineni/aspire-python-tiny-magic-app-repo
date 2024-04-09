"""
*************************************************
* classes to be used for testing factory instantiation
*************************************************
About:
1. Used in conjunction with test_factory_x.py

"""
from aspire_tinyapp.interfaces.objectinterfaces import (
    ISingleton, 
    IInitializable, 
    IInitializableWithArgs,
    IExecutor)

from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.publicinterfaces import factory
from aspire_tinyapp.publicinterfaces import config

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
param1="param1 value"
param2="param2 value"

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
* Test2, class2: TestSingletonClassWithConstructor
*************************************************
about:
1. Constructor with 2 args
2. Singleton

config entry:
[testclasses_class2]
classname="apptests.test_factory_classes.TestSingletonClassWithConstructor"
param1="param1 value"
param2="param2 value"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class2", None)
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

"""
*************************************************
* Test3, class3: TestMIClassWithConstructor
*************************************************
about:
1. Constructor with 2 args
2. Multi-instance

config entry:
[testclasses_class3]
classname="apptests.test_factory_classes.TestMIClassWithConstructor"
param1="param1 value"
param2="param2 value"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class3", None)
"""
class TestMIClassWithConstructor():
    def __init__(self, param1: str, param2: str):
        self.param1 = param1
        self.param2 = param2
        log.info("TestMIClassWithConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test3():
    obj1 = factory.getObjectAbsolute("testclasses_class3", None)
    log.prettyPrintObject(obj1)

    obj2 = factory.getObjectAbsolute("testclasses_class3", None)
    log.prettyPrintObject(obj2)

"""
*************************************************
* Test4, class4: TestMIClassNoConstructor
*************************************************
about:
1. No Constructor
2. Multi-instance

config entry:
[testclasses_class4]
classname="apptests.test_factory_classes.TestMIClassNoConstructor"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class4", None)
"""
class TestMIClassNoConstructor():
    def __init__(self):
        log.info("TestMIClassNoConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test4():
    obj1 = factory.getObjectAbsolute("testclasses_class4", None)
    log.prettyPrintObject(obj1)

    obj2 = factory.getObjectAbsolute("testclasses_class4", None)
    log.prettyPrintObject(obj2)

"""
*************************************************
* Test5, class5: TestClassWithInitializer
*************************************************
about:
1. No Constructor
2. Singleton
3. Initializable

config entry:
[testclasses_class5]
classname="apptests.test_factory_classes.TestClassWithInitializer"
param1="param1 value"
param2="param2 value"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class5", None)
"""
class TestClassWithInitializer(ISingleton, IInitializable):
    # Variable to hold the root context in the configruation file
    # in this case it will point to "testclasses_class5"
    contextRoot: str

    # you can then use to read the following
    param1: str
    param2: str

    def __init__(self):
        self.name = "TestClassWithInitializer"
        log.info("TestClassWithInitializer constructor called")

    # implementing the IInitializable interface
    def initialize(self, rootContext: str) -> None:
        self.contextRoot = rootContext
        param1 = config.getValue(rootContext + ".param1")
        param2 = config.getValue(rootContext + ".param2")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test5():
    obj = factory.getObjectAbsolute("testclasses_class5", None)
    log.prettyPrintObject(obj)

