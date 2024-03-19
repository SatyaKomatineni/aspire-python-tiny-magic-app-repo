"""
*************************************************
* Goal: How to load modules and classes dynamically
*************************************************
1. Provide a set of services for dynamically loading classes
2. Given a classame and a module specification
3. load the module
4. instantiate the class

"""
"""
*************************************************
* CodeGen section
*************************************************

First question:
if I want to specify a class to be instantiated dynamically from a configuration file like TOML, how to specify that classname so that an object can be created dynamically?

1. write me a function: load_class(full_class_name) 
    2. it should return an instance of that class assuming a no arg constructor
    3. Do not handle any exceptions in this class and propagate them
3. write second function: load_class_with_default(full_class_name: str, default_object: Any) 
    4. This should return the default object if there is an exception
    5. Exceptions should be logged in this second function
    5. Handle if you can specific exceptions that could result from the previous call and adjust the log messages
    5. The second function should call the first function to try to instantiate the object
    6. Assume the log function is named "log(exception, meaningful_message)" that knows how to log
6. functions should have type hints for their return values
7. write a test function as well that can exercise the second function
    8. Assume a simple fully qualified class name

"""

"""
*************************************************
* Actual code
*************************************************
"""

from baselib import baselog as log

import importlib
from typing import Any, Type
from baselib.objectinterfaces import ISingleton

def isSingleton(cls: Type[Any]) -> bool:
    return issubclass(cls,ISingleton)

def isMultiInstance(cls: Type[Any]) -> bool:
    return not isSingleton(cls)

def create_class_instance(cls: Type[Any]) -> Any:
    return cls()

def load_class(full_class_name: str) -> Any:
    """
    Loads and instantiates a class by its fully qualified name assuming a no-arg constructor.
    Exceptions are propagated.

    :param full_class_name: The fully qualified class name (e.g., 'my_package.my_module.MyClass')
    :return: An instance of the class.
    """
    module_name, class_name = full_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    cls: Type[Any] = getattr(module, class_name)
    return cls

def create_class_instance_with_default(full_class_name: str, default_object: Any) -> Any:
    """
    Attempts to instantiate a class by its fully qualified name,
    returning a default object if an exception occurs. Specific exceptions are logged with adjusted messages.

    :param full_class_name: The fully qualified class name.
    :param default_object: The default object to return in case of an exception.
    :return: An instance of the class or the default object if instantiation fails.
    """
    try:
        cls = load_class(full_class_name)
        obj = create_class_instance(cls)
        return obj

    except ModuleNotFoundError as e:
        log.logException(f"Module not found while attempting to load {full_class_name}", e)
    except AttributeError as e:
        log.logException(f"Class not found in the module while attempting to load {full_class_name}", e)
    except Exception as e:
        log.logException(f"Failed to load and instantiate {full_class_name} due to an unexpected error", e)
    return default_object

"""
*************************************************
* Reflection methods
*************************************************
""" 
def _createObjWithInit(cls: Type[Any], args: dict[str,Any]) -> Any:
    return cls(**args)

def _testCreateObjwithInit():
    cls = load_class("baselib.factoryutils.TestClass")
    argDict = {"arg1": "hello", "arg2": 5, "additional_org": "additional_stuff", "and more": "stuff"}
    obj = _createObjWithInit(cls, argDict)
    log.prettyPrintObject(obj)

    log.ph1("Direct instantiation test")
    obj = TestClass("hello", 1)
    log.prettyPrintObject(obj)

class TestClass():
    arg1: str
    arg2: int
    defaultarg: str
    def __init__(self, arg1: str, arg2: int, defaultarg: str = "charge", **kwargs: dict[str, Any]):
        self.arg1 = arg1
        self.arg2 = arg2
        self.defaultarg = defaultarg
        log.prettyPrintDictionary(kwargs)

"""
*************************************************
* Base testing support
*************************************************
"""
def test():
    _testCreateObjwithInit()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()