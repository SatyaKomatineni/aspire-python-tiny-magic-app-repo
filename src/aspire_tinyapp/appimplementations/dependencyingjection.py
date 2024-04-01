from typing import Any, Type 
from aspire_tinyapp.appimplementations.defaultfactory import DefaultFactory
from aspire_tinyapp.baselib import factoryutils as factoryutils
import logging
from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.baselib.factoryutils import SimpleParam
from aspire_tinyapp.interfaces.objectinterfaces import IDI
"""
*************************************************
* DependencyInjectionFactory: Instantiate a class by calling its contructor
*************************************************
Goal:

1. Use config_root_context to get the class parameters to resolve dependencies
2. objectargs are the arguments passed by the client
3. However the objectargs are unlikely to be used at thsi time. May be in the future

Inputs:
1. cls: The class to be instantiated
2. config_root_context: The root context in the configuration file where the parameters are stored
3. objectargs: Additional pass through arguments passed by the client. 
    often not used.
    Used in the DefaultFactory but not in this class
    This determination is done in default factory by looking at the "initialize" method of the class

Logic:
1. Find out what the parameters are for the constructor
2. Use the factoryutils module methods to find out the parameters
3. If there are no parameters just instantiate the class and return it
4. If there are parameters then get the values from the configuration
5. Create a dictionary of parameters
6. Instantiate the class with the parameters dictionary
7. Return the instance

Usage:
1. This can be instantiated from the config file
2. Or it can be instantiated from application object as a default factory
3. For now it is used as a default factory
"""

# Rest of the code
class DependencyInjectionFactory(DefaultFactory):
    """
    Overrirde's the DefaultFactory's _instantiateClass method
    """
    def _instantiateClass(self, cls: Type[Any], config_root_context: str, objectargs: Any) -> Any:
        # Get the parameters of the constructor
        paramList = factoryutils._getConstructorParams(cls)
        if not self._isThereAConstructor(cls, paramList):
            # No constructor. Just instantiate the class
            instance = cls()
            return instance

        # Get the parameter values from the configuration
        # Create a dictionary of parameters
        paramDict: dict[str, Any] = self._getParamDictionary(paramList, config_root_context)

        #instantiating the class
        instance = cls(**paramDict)
        return instance

    """
    1. Get the parameters from the configuration
    2. ignore kwargs for now
    3. config is expected to be case insensitive
    """
    def _getParamDictionary(self, paramList: list[factoryutils.SimpleParam], config_root_context: str) -> dict[str, Any]:
        paramDict: dict[str, Any] = {}
        for param in paramList:
            name = param.name
            # if name is kwargs or args then ignore it
            if name == "args":
                log.warn("args detected. Not handling it yet")
                continue
            if name == "kwargs":
                log.warn("kwargs detected. Not handling it yet")
                continue
            # param is a valid parameter
            paramvalue = self._getParamFromConfig(name, config_root_context)
            paramDict[name] = paramvalue
        return paramDict
    
    """
    1. Get the parameter value from the configuration
    2. config is expected to be case insensitive
    3. The parameters are expected to be in the config file next to config_root_context
    4. The parameter name is expected to be in the format: config_root_context.name
    5. uses the base class _getConfig method to get the config object
    """
    def _getParamFromConfig(self, name: str, config_root_context: str) -> Any:
        config = self._getConfig()
        paramValue = config.getValueAsObject(config_root_context + "." + name)
        return paramValue

    """
    1. Check if there is a constructor
    2. if the paramList is empty then there is no constructor
    """
    def _isThereAConstructor(self, cls: Type[Any], paramList: list[SimpleParam]) -> bool:
        #return true if there are parameters and the list is not empty
        return len(paramList) > 0
    
"""
*************************************************
* End: DependencyInjectionFactory
*************************************************
"""