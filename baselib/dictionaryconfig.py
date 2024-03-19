"""
*************************************************
* DictionaryConfig
*************************************************
Goal:
1. Implment IConfig
2. Acts as a base class for all dicionary based config implementations
3. Most implementations will extend this
4. An abstract class
5. Specializes the derived class through hook method: getDictionary

Derived classes:
1. TOMLConfig: Uses TOML configuration

Implementation:
1. Extends IConfig
2. Also extends IInitializable
3. As this is a factory object
4. Derived classes will provide the dictionary

"""

"""
*************************************************
* CodeGen
*************************************************
Create a class DictionaryConfig

1. An abstract class
2. has a private variable: dataDictionary: dict[str, Any]

3. has an abstract method called getDictionary() -> dict [str, Any]

4. Extends 2 abstract classes with respective overridden methods:
    InitializableWithArgs
        initializeWithOrgs(rootContext: str, args: Any) -> None
    IConfig
        def getValueAsObject(self, key:str) -> Any

5. Implement getValueAsObject() this way
    return the value for the given key from the local dataDictionary
    throws an exception if key not found with text: key not found with the key name

6. The initializeWithArgs() method calls the getDictionary(args) method to get and set the local variable
"""

"""
*************************************************
* Source code
*************************************************
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from baselib.objectinterfaces import IInitializableWithArgs
from baselib.configinterface import IDictionaryConfig

class DictionaryConfig(IInitializableWithArgs, IDictionaryConfig, ABC):
    _dataDictionary: Dict[str, Any]

    @abstractmethod
    def _getDictionary(self, args: Any) -> Dict[str, Any]:
        pass

    def initializeWithArgs(self, rootContext: str, args: Any) -> None:
        self._dataDictionary = self._getDictionary(args)

    def getValueAsObject(self, key: str) -> Any:
        if key in self._dataDictionary:
            return self._dataDictionary[key]
        else:
            raise KeyError(f"Key not found: {key}")
        
    def getKeyValuesAsDictionary(self) -> dict[str, Any]:
        return self._dataDictionary

"""
*************************************************
* TOMLConfig
*************************************************
"""
from baselib import configutils as configutils
from baselib import baselog as log
from typing import cast

class TOMLConfig(DictionaryConfig):
    def _getDictionary(self, args: Any = None) -> Dict[str, Any]:
        """
        1. validate args
        2. read config file
        3. flatten the dictionary
        4. return the flattened dictionary
        5. Use the configutils to do most of the work
        """
        log.validate_not_null_or_empty(args)
        log.assertType(args,str,"configuration filename needs to be a string")
        configfilename: str = cast(str, args)
        return configutils.getTOML_flattened_dictionary(configfilename)



"""
*************************************************
* Config Classes
*************************************************
tbd.
"""
class BaseTOMLConfig(TOMLConfig):
    def __init__(self, fq_config_filename: str):
        super().initializeWithArgs("",fq_config_filename)
    