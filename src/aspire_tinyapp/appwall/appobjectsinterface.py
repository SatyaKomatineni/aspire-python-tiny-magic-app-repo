"""
*************************************************
* AppObjects
*************************************************
Goal:
1. Easy access to operations on application objects
2. Uses ApplicationHolder as the store for the app objects
"""
from src.aspire_tinyapp.interfaces.loginterface import ICoreLog
from src.aspire_tinyapp.interfaces.configinterface import IConfig
from src.aspire_tinyapp.interfaces.factoryinterface import IFactory
from appwall.appholder import ApplicationHolder
from src.aspire_tinyapp.baseimpl import baselog as log
from src.aspire_tinyapp.interfaces.configinterface import IDictionaryConfig

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
