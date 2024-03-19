"""
*************************************************
* Imports
*************************************************
"""
from baselib import baselog as log
from abc import ABC, abstractmethod
from typing import Any


"""
*************************************************
* Code gen comments
*************************************************
"""

"""
Create me the following:
1. An abstract class called IConfig
2. It will have the following methods:
4. overridable method: getValueWithDefault (key: str, defaultValue: str) -> str
    this will call the getValue() and if an exception is thrown return the default value
    default value can None
5. abstract method: getValue(key: str) -> str

"""

"""
*************************************************
* Code
*************************************************
"""

class IConfig(ABC):
    """
    1. Returns a string
    2. Calls getValue with an expectation of string
    2. if an exception return the default string
    """
    def getValueWithDefault(self, key: str, defaultValue: str) -> str:
        """
        Tries to get the value for the given key.
        If an exception is thrown, returns the defaultValue.
        """
        try:
            # Attempt to call the abstract getValue method
            return self.getValue(key)
        except Exception as e:
            log.logException(f"Key not found: {key}",e)
            return defaultValue

    """
    1. Returns a string
    2. calls getValuteAsObject
    2. Coarse an object to string if not string
    3. Can throw an exception if not found
    """
    def getValue(self, key: str) -> str:
        value = self.getValueAsObject(key)
        if isinstance(value, str):
            return value
        # Not a string bject
        log.warn(f"The value for key {key} is not a string. it is {value}. Coarsing")
        return str(value)

    """
    1. Returns an object, often a string
    2. Less used method. Prefer to use string versions of it
    3. calls getValuteAsObject
    4. if an exception returns the default object
    """
    def getValueAsObjectWithDefault(self, key:str, defaultValue: Any) -> Any:
        try:
            return self.getValueAsObject(key)
        except Exception as e:
            log.logException(f"Key not found: {key}",e)
            return defaultValue

    """
    1. Most generic method
    2. An object version
    3. Prefer to use the string version variants of this method 
    """
    @abstractmethod
    def getValueAsObject(self, key:str) -> Any:
        pass


"""
*************************************************
* For debugging purposes
*************************************************
"""
class IDictionaryConfig(IConfig):
    @abstractmethod
    def getKeyValuesAsDictionary(self) -> dict[str, Any]:
        pass
