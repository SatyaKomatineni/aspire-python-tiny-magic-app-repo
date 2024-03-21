"""
*************************************************
* Contains interfaces and tags to support Factory implementation
*************************************************
1. IInitializable
2. IInitializableWithArgs
3. ISingleton

Each of these interfaces and their goals are listed below one by one

"""
"""
*************************************************
* IInitializable
*************************************************
Goal:
1. Allow initialization of objects instantiated dynamically
2. Usually from configuration files
3. Takes the context or the root configuration name underwhich this object is to be initialized from

Usage:
1. Most base classes that wants to be configurable inherit this class
2. Classes that wants to be singletons
3. Classes that are unique to a context

Alternatives not taken:
1. I could pass a **kwargs as an additional argument
2. But I don't see when I would do that
3. If needed in the future, use another interface that is more tuned to that need

Related classes:
1. IConfig
2. IFactory
3. IApplication
4. IExecutor (aka: ICreator)

"""

"""
*************************************************
* codegen
*************************************************
Create an abstract class: IInitializable
abstract methods:
    initialialize(rootContext: str) -> None

"""
from abc import ABC, abstractmethod
from typing import Any

class IInitializable(ABC):
    @abstractmethod
    def initialize(self, rootContext: str) -> None:
        """
        Abstract method to initialize the object with a root context.

        :param rootContext: A string representing the root context for initialization.
        """
        pass
"""
1. Experimental
2. Some specialized classes that are better of taking the arguments in initialization
3. and not depend on the configuration  file for some primary parameters
4. For example a Config class that requires a config file spec
"""
class IInitializableWithArgs(ABC):
    @abstractmethod
    def initializeWithArgs(self, rootContext: str, args: Any) -> None:
        pass

"""
*************************************************
* ISingleton
*************************************************
Goal:
1. Act as a tag to know if the class is a singleton
"""
from typing import Type, Any

class ISingleton():
    @staticmethod
    def isSingleton(classObj: Type[Any]) -> bool:
        return issubclass(classObj,ISingleton)

"""
*************************************************
* IExecutor
*************************************************
"""
class IExecutor(ABC):
    @abstractmethod
    def execute(self, config_root_context: str, args: Any) -> Any:
        pass

    @staticmethod
    def isSame(classObj: Type[Any]) -> bool:
        return issubclass(classObj, IExecutor)
