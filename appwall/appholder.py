"""
*************************************************
* ApplicationHolder class
*************************************************
Goal:
1. Holds the application singleton object
2. Initializes the application through a config file
3. This must be done before this application is used
4. Starts with a bootstrap app and then loads the real app from config file

"""
from baselib.applicationinterface import IApplication
class ApplicationHolder():
    appconfig_filename: str = ""
    application: IApplication | None = None

    @staticmethod
    def getApplication() -> IApplication:
        return ApplicationHolder.application #type:ignore
    
    @staticmethod
    def setBaseApplication(configfilename: str, baseapp: IApplication):
        ApplicationHolder.appconfig_filename = configfilename
        ApplicationHolder.application = baseapp

    @staticmethod
    def setRealApplication(realApp: IApplication):
        ApplicationHolder.application = realApp

