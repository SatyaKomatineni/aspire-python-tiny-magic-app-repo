from typing import Any, Type 
from aspire_tinyapp.appimplementations.defaultfactory import DefaultFactory
from aspire_tinyapp.baselib import factoryutils as factoryutils
import logging
from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.baselib.factoryutils import SimpleParam

"""
*************************************************
* DependencyInjectionFactory: Instantiate a class by calling its contructor
*************************************************
Goal:

1. Use config_root_context to get the configuration to resolve dependencies
2. objectargs are the arguments passed by the client
3. However the objectargs are unlikely to be used at thsi time. May be in the future

Logic:
1. Find out what the parameters are for the constructor
2. Use the factoryutils module methods to find out the parameters
3. If there are no parameters just instantiate the class and return it
4. If there are parameters then get the values from the configuration
5. Create a dictionary of parameters
6. Instantiate the class with the parameters dictionary
7. Return the instance

"""

# Rest of the code
class DependencyInjectionFactory(DefaultFactory):
    def _instantiateClass(self, cls: Type[Any], config_root_context: str, objectargs: Any) -> Any:
        # Get the parameters of the constructor
        paramList = factoryutils._getConstructorParams(cls)
        if not self._isThereAConstructor(paramList):
            # No constructor. Just instantiate the class
            instance = cls()
            return instance

        # Get the parameter values from the configuration
        # Create a dictionary of parameters
        paramDict: dict[str, Any] = self._getParamDictionary(paramList, config_root_context)

        #instantiating the class
        instance = cls(**paramDict)
        return instance

    def _getParamDictionary(self, paramList: list[factoryutils.SimpleParam], config_root_context: str) -> dict[str, Any]:
        paramDict: dict[str, Any] = {}
        for param in paramList:
            name = param.name
            if name == "kwargs":
                log.warn("kwargs detected. Not handling it yet")
                continue
            # param is a valid parameter
            paramvalue = self._getParamFromConfig(name, config_root_context)
            paramDict[name] = paramvalue
        return paramDict
    
    def _getParamFromConfig(self, name: str, config_root_context: str) -> Any:
        config = self._getConfig()
        paramValue = config.getValueAsObject(config_root_context + "." name)
        return paramValue

    def _isThereAConstructor(self, paramList: list[SimpleParam]) -> bool:
        #return true if there are parameters and the list is not empty
        return len(paramList) > 0

"""
*************************************************
* End: DependencyInjectionFactory
*************************************************
"""