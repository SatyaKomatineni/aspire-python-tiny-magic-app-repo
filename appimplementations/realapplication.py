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

"""
from baselib.applicationinterface import IApplication
from baselib.loginterface import TrivialLog, ICoreLog
from baselib.configinterface import IConfig
from baselib.factoryinterface import IFactory
from baselib.dictionaryconfig import BaseTOMLConfig
from appimplementations.defaultfactory import DefaultFactory
from typing import Any, cast
from baselib.configinterface import IConfig
from appwall.appholder import ApplicationHolder
from baselib.appconfignames import ApplicationObjectNames
from baselib import baselog as log

from baselib.objectinterfaces import (ISingleton, IInitializableWithArgs)

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