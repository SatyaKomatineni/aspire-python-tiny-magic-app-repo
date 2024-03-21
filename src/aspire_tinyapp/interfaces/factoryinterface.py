"""
*************************************************
* Inroduction
*************************************************
Goal:
1. Create an interface to create objects
2. usuall based on configuration files
3. A singleton
4. Replacable with future implementations
5. Can support many kinds of dependency injection
6. Closely works with IApplication and its interfaces

Related classes:
1. config, log, factory, application, applicationholder

Derived classes:
AbsFactory: 
1. Use this derive further
2. This was separated to simplify circular dependency with logging

Related classes:
BaseFactory
1. Used to break dependency and does not derive from this class
2. Its needs are simpler

Documentation:
1. tbd
2. tbd

Possibilities:
1. Provide for configuration data objects
2. By extending or tagging as ConfigObject the factory will fill and return
3. One way to objectify configuration with or without behavior
4. A future factory implementation can do that
"""
"""
*************************************************
* Code spec
*************************************************
1. Create an abstract clas with name IFactory
2. Abstractt Methods
    public Object getObjectAbsolute(String identifier, Object args)

3. Regular method
    1. public getObjectInvocationPrefix()
        should return "request"

    2. public Object getObject(String identifier, Object args)
        call getObjectInvocationPrefix() and add its output to the identifier  to call getObjectAbsolute()

    3. public Object getObjectWithDefault(String identifier, Object args, Object defaultObject)
    This method should call the getObject() and 
        if that throws exception
        log the exception
        return the default
    if it doesn't throw the exception return the object from getObject()

"""

from abc import ABC, abstractmethod
from typing import Any

class IFactory(ABC):

    @abstractmethod
    def getObjectAbsolute(self, identifier: str, args: Any) -> Any:
        """
        Abstract method to be implemented by subclasses.
        """
        pass

    def getObjectInvocationPrefix(self) -> str:
        """
        Regular method that returns the invocation prefix.
        """
        return "request."

    def getObject(self, identifier: str, args: Any) -> Any:
        """
        Calls getObjectAbsolute with a modified identifier.
        """
        modified_identifier = self.getObjectInvocationPrefix() + identifier
        return self.getObjectAbsolute(modified_identifier, args)

    @abstractmethod
    def getObjectWithDefault(self, identifier: str, args: Any, defaultObject: Any) -> Any:
        """
        Attempts to call getObject and returns defaultObject if an exception occurs.
        """
        pass       

    @abstractmethod
    def getObjectAbsoluteWithDefault(self, identifier: str, args: Any, defaultObject: Any) -> Any:
        """
        Attempts to call getObject and returns defaultObject if an exception occurs.
        """
        pass
    