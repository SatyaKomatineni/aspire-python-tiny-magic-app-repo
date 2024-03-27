
"""
*************************************************
* Dependencies
*************************************************
1. core inerfaces
2. baselib
"""
from aspire_tinyapp.interfaces.loginterface import ICoreLog
from typing import Optional
from aspire_tinyapp.interfaces.objectinterfaces import (ISingleton, IInitializable)

"""
*************************************************
* Trivial log
*************************************************
"""

from aspire_tinyapp.baselib import baselog as log
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
