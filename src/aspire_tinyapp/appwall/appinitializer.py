
from aspire_tinyapp.appwall.appholder import ApplicationHolder
from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.baseimpl.baseapplication import BaseApplication
from aspire_tinyapp.interfaces.appconfignames import ApplicationObjectNames
from aspire_tinyapp.appimplementations.realapplication import DirectDefaultApplication

class AppInitializer():
    @staticmethod
    def initializeApplication(config_filename: str):
        log.validate_not_null_or_empty(config_filename)
        ApplicationHolder.setBaseApplication(config_filename, BaseApplication(config_filename))
        log.info("Creating Real Appliatin object")
        ApplicationHolder.setRealApplication(AppInitializer._createRealApplication(config_filename))

    @staticmethod
    def _createRealApplication(config_filename: str):
        fact = ApplicationHolder.application.getFactory() #type:ignore
        try:
            return fact.getObjectAbsolute(ApplicationObjectNames.APPLICATION_OBJ_NAME, ApplicationHolder.appconfig_filename)
        except Exception as e:
            log.logException("No config app object in config file. Creating DirectDefaultApplication", e)
            return DirectDefaultApplication(config_filename)    