
"""
Create an abtract class

1. name it IApplication
2. Abstract Methods:
    getConfig() -> IConfig
    getFactory() -> IFactory
    getLog() -> ILong

Create another class 
1. ApplicationHolder
2. class variables
    application_config_filename: str
    application_instance: IApplication
3. Methods
    static method: initialize(configfilename: str)

"""

from abc import ABC, abstractmethod
from baselib.configinterface import IConfig
from baselib.loginterface import ICoreLog
from baselib.factoryinterface import IFactory

class IApplication(ABC):

    @abstractmethod
    def getConfig(self) -> IConfig:
        """Return the application configuration."""
        pass

    @abstractmethod
    def getFactory(self) -> IFactory:
        """Return the factory used by the application."""
        pass

    @abstractmethod
    def getLog(self) -> ICoreLog:
        """Return the logging interface used by the application."""
        pass



