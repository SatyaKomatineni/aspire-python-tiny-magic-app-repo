"""
*************************************************
* TOMLConfig
*************************************************
Dependencies:
intefaces module
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from aspire_tinyapp.interfaces.objectinterfaces import IInitializableWithArgs
from aspire_tinyapp.interfaces.configinterface import IDictionaryConfig
from aspire_tinyapp.interfaces.dictionaryconfig import DictionaryConfig
from aspire_tinyapp.baselib import configutils as configutils

from aspire_tinyapp.baselib import baselog as log
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
    