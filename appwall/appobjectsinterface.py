"""
*************************************************
* AppObjects
*************************************************
Goal:
1. Easy access to operations on application objects
2. Uses ApplicationHolder as the store for the app objects
"""
from baselib.loginterface import ICoreLog
from baselib.configinterface import IConfig
from baselib.factoryinterface import IFactory
from appwall.appholder import ApplicationHolder
from baselib import baselog as log
from baselib.configinterface import IDictionaryConfig

class AppObjects():
    @staticmethod
    def getConfig() -> IConfig:
        return ApplicationHolder.getApplication().getConfig()
    
    @staticmethod
    def getLog() -> ICoreLog:
        return ApplicationHolder.getApplication().getLog()
    
    @staticmethod
    def getFact() -> IFactory:
        return ApplicationHolder.getApplication().getFactory()
    
    @staticmethod
    def printConfig():
        cfg = AppObjects.getConfig()
        if isinstance(cfg, IDictionaryConfig):
            d = cfg.getKeyValuesAsDictionary()
            log.prettyPrintDictionary(d)
