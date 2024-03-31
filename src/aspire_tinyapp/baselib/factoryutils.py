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

from aspire_tinyapp.baselib import baselog as log

import importlib
from typing import Any, Type
from src.aspire_tinyapp.interfaces.objectinterfaces import ISingleton
import inspect

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
"""
*************************************************
* Creates an object by calling the "init" method
* Exepects to know the arguments to pass to the init method
* Useful for loadign data classes from configuration files
* Can also be used for factory classes where the constructor is virtualized
*************************************************
"""
def _testCreateObjwithInit():
    cls = load_class("aspire_tinyapp.baselib.factoryutils.TestClass")

    # case: with kwargs as well
    # you cannot pass additional args if the class doesn't have kwargs
    # additional args can be just key value pairs and not a dictionary necesssarily
    # The unused params will go as kwargs (i think. tested. that is correct)
    #argDict = {"arg1": "hello", "arg2": 5, "additional_org": "additional_stuff", "and more": "stuff"}

    # case: without kwargs in the class
    # it will fail if you pass additional args
    # only the args that are expected will need to be passed
    #argDict = {"arg1": "hello", "arg2": 5, "additional_org": "additional_stuff", "and more": "stuff"}

    #case with the default args
    # default org will override the default value in the class
    # additional args passed as kwargs
    # if kwargs are ommitted in the class, passing them will result in an error
    # 
    argDict = {"arg1": "hello", "arg2": 5, 
               "defaultarg" : "default org", 
               "additional_org": "additional_stuff", 
               "and more": "stuff"}
    log.ph1("Reflection instantiation test")
    obj = _createObjWithInit(cls, argDict)
    log.info("Object field values")
    log.prettyPrintObject(obj)

    log.ph1("Direct instantiation test")
    obj = TestClass("hello", 1)
    log.prettyPrintObject(obj)

class TestClass():
    arg1: str
    arg2: int
    defaultarg: str
    def __init__(self, arg1: str
                 ,arg2: int, 
                 defaultarg: str = "charge"
                 , **kwargs: dict[str, Any]
                 ):
        self.arg1 = arg1
        self.arg2 = arg2
        self.defaultarg = defaultarg
        log.info("Additional arguments")
        log.prettyPrintDictionary(kwargs)

"""
*************************************************
* A function to tell me the parameters of a python class constructor
*************************************************
1. Should return a list of parameters
2. each parameter should be a tuple of (name, type, default)
3. Should handle the case where there are no parameters
4. should return an empty list in that case
5. I just need to know if the param has a default or not
6. I don't need "self" as a parameter
7. I also just need the classtype as a "string" and not the actual class
"""

class SimpleParam():
    def __init__(self, name: str, type: str, default: bool):
        self.name = name
        self.type = type
        self.default = default

    def __repr__(self) -> str:
        return f"Name: {self.name}, Type: {self.type}, Default: {self.default}"

def _getConstructorParams(cls) -> list[SimpleParam]:
    init_signature = inspect.signature(cls.__init__)
    params = []
    for name, param in init_signature.parameters.items():
        if name == 'self':
            continue
        param_type = param.annotation.__name__ if param.annotation is not param.empty else 'No Type Info'
        has_default = param.default is not param.empty
        param = SimpleParam(name, param_type, has_default)
        params.append(param)
    return params

def _testGetConstructorParams():
        cls = load_class("aspire_tinyapp.baselib.factoryutils.TestClass")
        params = _getConstructorParams(cls)
        log.info("Constructor parameters")
        log.info(f"{params}")


    
"""
*************************************************
* Base testing support
*************************************************
"""
def test():
    #_testCreateObjwithInit()
    _testGetConstructorParams()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()