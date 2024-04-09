
"""
*************************************************
* Provide a public interface for the config object
*************************************************
Goals:
1. Acts as a true interface
2. No need to know the details of the implementation. In fact hide them.
3. A static kind of interface
4. A bit like APIs
"""
from aspire_tinyapp.appwall.appobjectsinterface import AppObjects
from aspire_tinyapp.appwall.appobjectsinterface import IConfig
from typing import Any

"""
*************************************************
* Initialize the global config object
*************************************************
"""

def _config() -> IConfig:
    return AppObjects.getConfig()

# This won't work because the factory object is not initialized
# so it has to be a method invocation
# use _config() instead
# global_config: IConfig  = _getGlobalConfig()

"""
*************************************************
* Standalone functions for IConfig methods
*************************************************
"""

def getValueWithDefault(key: str, defaultValue: str) -> str:
    return _config().getValueWithDefault(key, defaultValue)

def getValue(key: str) -> str:
    return _config().getValue(key)

def getValueAsObjectWithDefault(key:str, defaultValue: Any) -> Any:
    return _config().getValueAsObjectWithDefault(key, defaultValue)

def getValueAsObject(key:str) -> Any:
    return _config().getValueAsObject(key)

"""
*************************************************
* Interpreted functions for IConfig methods
*************************************************
tbd
"""