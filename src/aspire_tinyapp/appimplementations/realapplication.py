"""
*************************************************
* ConfigApplication: Driven by configuration
*************************************************
Goal:
1. Config Application
2. One that is constructed from the configuration file
3. Gets Log, Config, and Factory from app config file

Related classes:

ApplicationHolder
AppObjects

Why does it depend on BaseFactory?:

1. Although it can be obtained from the config in a derived fashion,
2. it is rare that this object needs to be changed
3. It is a good idea to have a default factory that can be used
4. Its behavior, nevertheless, is to obtain the 3 dependent objects from the config
5. That is why it needs the BaseFactory which it gets it from ApplicationHolder

"""

"""
*************************************************
* Interfaces
*************************************************
"""
from aspire_tinyapp.interfaces.applicationinterface import IApplication
from aspire_tinyapp.interfaces.loginterface import ICoreLog
from aspire_tinyapp.interfaces.configinterface import IConfig
from aspire_tinyapp.interfaces.factoryinterface import IFactory
from aspire_tinyapp.interfaces.configinterface import IConfig

"""
*************************************************
* Implementations
*************************************************
"""
from aspire_tinyapp.baseimpl.default_base_logs import TrivialLog
from aspire_tinyapp.baseimpl.base_tomlconfig import BaseTOMLConfig
from aspire_tinyapp.appimplementations.defaultfactory import DefaultFactory
from aspire_tinyapp.appwall.appholder import ApplicationHolder

from typing import Any, cast
from aspire_tinyapp.interfaces.appconfignames import ApplicationObjectNames
from aspire_tinyapp.baselib import baselog as log

from src.aspire_tinyapp.interfaces.objectinterfaces import (ISingleton, IInitializableWithArgs)

class DefaultConfigApplication(IApplication,ISingleton, IInitializableWithArgs):

    config: IConfig
    log: ICoreLog
    factory: IFactory
    configRootContext: str

    """
    From IInitializableWithArgs
    """
    def initializeWithArgs(self, rootContext: str, args: Any) -> None:
        self.configRootContext = rootContext
        self._init(cast(str,args))

    """
    *************************************************
    * Init (local): called by initialzablewith args
    *************************************************
    """
    def _init(self, configfilename: str):

        self.log = self._createLog()
        self.config = self._createConfig(configfilename)
        self.factory = self._createFactory(self.config)

    def _getBootstrapFactory(self) -> IFactory:
        fact = ApplicationHolder.application.getFactory() #type:ignore
        return fact

    """
    *************************************************
    * Interface
    *************************************************
    """
    def getConfig(self) -> IConfig:
        return self.config

    def getFactory(self) -> IFactory:
        return self.factory

    def getLog(self) -> ICoreLog:
        return self.log

    """
    *************************************************
    * Creation
    *************************************************
    """
    def _createLog(self) -> ICoreLog:
        fact = self._getBootstrapFactory()
        try:
            # Use TrivialConfigLog as an example to create one of these
            return fact.getObjectAbsolute(ApplicationObjectNames.LOG_OBJECT_NAME, None)
        except Exception as e:
            log.logException("Failed to create a log object", e)
            return TrivialLog()

    def _createConfig(self, configfilename: str) -> IConfig:
        fact = self._getBootstrapFactory()
        try:
            # Use TOMLConfig as an example to create one of these via config
            return fact.getObjectAbsolute(ApplicationObjectNames.CONFIG_OBJ_NAME, configfilename)
        except Exception as e:
            log.logException("Failed to create a config object", e)
            return BaseTOMLConfig(configfilename)
        
    def _createFactory(self, config: IConfig):
        fact = self._getBootstrapFactory()
        try:
            # Use TOMLConfig as an example to create one of these via config
            return fact.getObjectAbsolute(ApplicationObjectNames.FACTORY_OBJ_NAME, None)
        except Exception as e:
            log.logException("Failed to create a factory object", e)
            return DefaultFactory()


class DirectDefaultApplication(DefaultConfigApplication):
    def __init__(self, configfilename: str):
        super()._init(configfilename)