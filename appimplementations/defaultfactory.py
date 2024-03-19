"""
*************************************************
* DefaultFactory
*************************************************
Goal:
    1. A factory that knows how to instantiate
    2. Singletons
    3. Multi instance
    4. Call executors for dynamic output/pipelines
    5. Takes threading into consideration

Logic:
1. Create a factory class called DefaultFactory
2. Maintains a cache (dictionary) of singleton objects
3. Create a method called getObject(fqcn: str) -> Any
4. This mehtod takes a fully qualified classname as a string
5. The logic of this method is as follows
6. works with 3 interface tags
    1. IInitializable
    2. IExecutor
    3. ISingleton
7. case: if the fqcn is in the cache return its corresponding singleton object
8. case: if not
    1. create a class object (not the instance) by calling a method called load_class(fqcn)
    2. You can call a static method ISingleton.isSingleton() to see if the class is a singleton or a multi instance
    3. case: multi instance
        call an instance method called processSingleOrMultiInstance(obj: Any)
        return the output from that method 
    4. case: singleton
        1. lock the cache
        2. see if it is in the cache and if so return it and unlock
        3. log a message that we are creating a singleton of that type
        4. create the instance from the class object
        5. call an instance method called processSingleton(obj: Any)
        6. register the singleton in the cache
        7. unlock the cache
        8. return the singleton
    5. processSingleOrMultiInstance(obj: Any) -> Any
        1. if the obj is an instance of IInitializable call initialize() with args if needed
        2. if it implements IExecutor call its execute() method and get an object back
        3. Return the object to the caller
9. In the end this class should have the following
    1. A dictionary dict[str: Any] of named objects as a cache
    2. A method: getObject(fqcn) -> Any
    3. processSingleOrMultiInstance(obj: Any) -> Any

"""

import threading
import importlib
from typing import Any, Dict, Type
from baselib.factoryinterface import IFactory
from appwall.appobjectsinterface import AppObjects
from baselib.appconfignames import ConfigFactoryParamNames
from baselib import baselog as log
from baselib.objectinterfaces import ISingleton, IInitializable

from baselib.objectinterfaces import (
    IInitializable,
    IInitializableWithArgs,
    ISingleton,
    IExecutor
)

"""
*************************************************
* AbstractFactory
*************************************************
"""
class AbsFactory(IFactory, ISingleton, IInitializable):

    def getObjectWithDefault(self, identifier: str, args: Any, defaultObject: Any) -> Any:
        """
        Attempts to call getObject and returns defaultObject if an exception occurs.
        """
        try:
            return self.getObject(identifier, args)
        except Exception as e:
            print(f"Exception caught: {e}")  # Simple logging of the exception
            return defaultObject
        
    def getObjectAbsoluteWithDefault(self, identifier: str, args: Any, defaultObject: Any) -> Any:
        """
        Attempts to call getObject and returns defaultObject if an exception occurs.
        """
        try:
            return self.getObjectAbsolute(identifier, args)
        except Exception as e:
            print(f"Exception caught: {e}")  # Simple logging of the exception
            return defaultObject


# Assuming the preliminary interface definitions from the previous explanation

class DefaultFactory(AbsFactory, ISingleton, IInitializable):
    _cache: Dict[str, Any] = {}
    _lock = threading.Lock()

    configRootContext: str
    """
    *************************************************
    * Initialization and Contract methods
    *************************************************
    1. It doesn't need initialization for dependencies
    2. Assumes the BaseApplication object is in place while this is being constructed
    """    
    def __init__(self):
        self.configRootContext = ""

    def initialize(self, rootContext: str) -> None:
        self.configRootContext = rootContext

    """
    *************************************************
    * abstract methods for IFactory
    *************************************************
    """
    """
    1. Return an object based on singleton or multiinstance
    2. identifier: The absolute root in the config file where the desired object is anchored
    3. args: Based on the receiver pass on the arguments. Pass through args
    4. To know the nature of args look at the receiving class objects
    5. Entry method into this class
    """
    def getObjectAbsolute(self, identifier: str, args: Any) -> Any:
        #Figure out the classname
        config = AppObjects.getConfig()
        fqcn = config.getValue(identifier + "." + ConfigFactoryParamNames.CLASS_NAME)

        #get
        obj_instance = self._getObjectGivenClassname(fqcn,identifier,args)
        return obj_instance

    """
    *************************************************
    * Rest of the implementation
    *************************************************
    """
    """
    Given a fully qualified classname load its class 
    """
    @staticmethod
    def load_class(fqcn: str) -> Type[Any]:
        module_name, class_name = fqcn.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    
    """
    1. Given an object that is just loaded call its contracting methods
    2. The object can be a single or multiinstance
    3. Take into account initializable with or without args
    4. Take into account if it is a executor
    """
    @staticmethod
    def processSingleOrMultiInstance(obj: Any, config_root_context: str, objargs: Any) -> Any:
        if isinstance(obj, IInitializableWithArgs):
            # Assuming no args for simplicity; adjust as necessary
            obj.initializeWithArgs(config_root_context,objargs)
        elif isinstance(obj, IInitializable):
            obj.initialize(config_root_context)

        if isinstance(obj, IExecutor):
            return obj.execute(config_root_context, objargs)
        return obj
    
    """
    ***********************************************
    Goal:
    1. Given a classname load its class
    2. if a singleton put it in the cache
    3. call the contract methods
    4. It does this by calling other methods
    5. At the end return an object that is
        1. cached
        2. its obligatory methods executed

    Params:
    fqcn: fully qualified classname
    config_root_context: where this object is anchored in the config file
    objectargs: the client passed arguments meant for the instantiated object
    ***********************************************
    """
    def _getObjectGivenClassname(self, fqcn: str, config_root_context: str, objectargs: Any) -> Any:
        if fqcn in self._cache:
            return self._cache[fqcn]
        
        class_obj = self.load_class(fqcn)
        # Assuming ISingleton provides a means to check for singleton status; adjust as necessary
        if ISingleton.isSingleton(class_obj):
            with self._lock:
                if fqcn in self._cache:
                    return self._cache[fqcn]
                log.info(f"Creating a singleton of type: {fqcn}")
                instance = class_obj()
                instance = DefaultFactory.processSingleOrMultiInstance(instance, config_root_context, objectargs)
                self._cache[fqcn] = instance
                return instance
        else:
            instance = class_obj()
            return DefaultFactory.processSingleOrMultiInstance(instance, config_root_context, objectargs)


