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
from typing import Any
from dataclasses import dataclass

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
        self.param1 = config.getValue(rootContext + ".param1")
        self.param2 = config.getValue(rootContext + ".param2")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test5():
    obj = factory.getObjectAbsolute("testclasses_class5", None)
    log.prettyPrintObject(obj)

"""
*************************************************
* Test 6, class6: TestClassWithInitializerArgs
*************************************************
about:
1. No Constructor
2. Singleton
3. InitializableWithArgs

config entry:
[testclasses_class6]
classname="apptests.test_factory_classes.TestClassSIWithInitializerArgs"
param1="param1 value"
param2="param2 value"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class6", None)
"""
class TestClassSIWithInitializerArgs(ISingleton, IInitializableWithArgs):
    # Variable to hold the root context in the configruation file
    # in this case it will point to "testclasses_class5"
    contextRoot: str

    # you can then use to read the following
    param1: str
    param2: str
    param3_from_args: str

    def __init__(self):
        self.name = "TestClassWithInitializer"
        log.info("TestClassWithInitializer constructor called")

    # implementing the IInitializable interface
    def initializeWithArgs(self, rootContext: str, args: str) -> None:
        self.contextRoot = rootContext
        self.param1 = config.getValue(rootContext + ".param1")
        self.param2 = config.getValue(rootContext + ".param2")

        # this is the additional parameter that is passed in the args
        self.param3_from_args = args

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test6():
    obj = factory.getObjectAbsolute("testclasses_class6", "Third argument value")
    log.prettyPrintObject(obj)

"""
*************************************************
* Test 7, class 7: TestClassMIECWithInitializerArgs
*************************************************
about:
1. Explicit Constructor (C)
2. Multi Instance (MI)
3. Executor (E)
3. InitializableWithArgs

config entry:
[testclasses_class7]
classname="apptests.test_factory_classes.TestClassMIECWithInitializerArgs"
param1="param1 value"
param2="Send back hello world via execute method"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class7", None)
"""
class TestClassMIECWithInitializerArgs(IExecutor, IInitializableWithArgs):
    # Variable to hold the root context in the configruation file
    # in this case it will point to "testclasses_class5"
    contextRoot: str

    # you can then use to read the following
    param1: str
    param2: str
    param3_from_args: str

    def __init__(self, param1: str, param2: str):
        self.name = "TestClassMIECWithInitializerArgs"
        log.info("TestClassMIECWithInitializerArgs constructor called")
        self.param1 = param1
        self.param2 = param2

    # implementing the IInitializable interface
    def initializeWithArgs(self, rootContext: str, args: str) -> None:
        self.contextRoot = rootContext

        # this is the additional parameter that is passed in the args
        self.param3_from_args = args

    def execute(self, config_root_context: str, args: Any) -> Any:
        return self.param2

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test7():
    obj = factory.getObjectAbsolute("testclasses_class7", "Third argument value")
    log.info(f"Returned value from execute: {obj}")


"""
*************************************************
* Test 8, class 8: TestDataClass
*************************************************
about:
1. Explicit Constructor (C)
2. Multi Instance (MI)
3. A data class
4. Holds a set of configuration params

config entry:

[testclasses_class8]
classname="apptests.test_factory_classes.TestDataClass"
param_str="string value"
param_int_1=5
param_int_1=5.6
param_bool=True
param_list=[1,2,3]
param_dict={"key1":"value1", "key2":"value2"}

#how to get it
obj = factory.getObjectAbsolute("testclasses_class8", None)

"""

@dataclass
class TestDataClass:
    param_str: str
    param_int_1: int
    param_float: float
    param_bool: bool
    param_list: list[int]

    # init is auto generated by dataclass

def _test8():
    obj = factory.getObjectAbsolute("testclasses_class8", None)
    log.prettyPrintObject(obj)
