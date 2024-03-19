"""
*************************************************
* Goal
*************************************************
1. Act as a minimalist base interface for logging
2. Based on Aspire log

TBd:
1. is it better at this level
2. Or to define a LogWrapper that solidifies the contract interface?
3. such as info, log, etc.
4. Not sure yet

For now:
1. Go with the core idea
2. Come back later and enhance it

Derived classes:
1. TrivialLog

"""

"""
*************************************************
* CodeGen comments
*************************************************
Create me a python class

classname: ICoreLog

Abstract Methods:
    public void log(String message, String msgType);
    public void logE(Throwable t, cause: Optional[str]=None);
    public boolean isItNecessaryToLog(mesgType: str);

"""

from abc import ABC, abstractmethod
from typing import Optional

class ICoreLog(ABC):

    @abstractmethod
    def log(self, message: str, msgType: str) -> None:
        """
        Abstract method to log a message with a specific message type.
        """
        pass

    @abstractmethod
    def logE(self, t: Exception, cause: Optional[str] = None) -> None:
        """
        Abstract method to log exceptions, with an optional cause.
        """
        pass

    @abstractmethod
    def isItNecessaryToLog(self, msgType: str) -> bool:
        """
        Abstract method to determine if it is necessary to log a message of a specific type.
        Returns True if it is necessary, False otherwise.
        """
        pass

"""
*************************************************
* Trivial log
*************************************************
"""

from baselib import baselog as log
class TrivialLog(ICoreLog):

    def log(self, message: str, msgType: str) -> None:
        print(f"{msgType}:{message}")

    def logE(self, t: Exception, cause: Optional[str] = None) -> None:
        if cause:
            log.logException(cause, t)
        else:
            log.logException("Exception", t)

    def isItNecessaryToLog(self, msgType: str) -> bool:
        return True

"""
*************************************************
* TrivialConfigLog
*************************************************
"""
from baselib.objectinterfaces import (ISingleton, IInitializable)
class TrivialConfigLog(ICoreLog, ISingleton, IInitializable):

    #Use this to read additional logging related configuration
    configRootContext: str

    def initialize(self, rootContext: str) -> None:
        self.configRootContext = rootContext

    def log(self, message: str, msgType: str) -> None:
        print(f"{msgType}:{message}")

    def logE(self, t: Exception, cause: Optional[str] = None) -> None:
        if cause:
            log.logException(cause, t)
        else:
            log.logException("Exception", t)

    def isItNecessaryToLog(self, msgType: str) -> bool:
        return True
