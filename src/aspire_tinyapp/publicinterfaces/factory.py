
"""
*************************************************
* Provide a public interface for the factory object
*************************************************
Goals:
1. Acts as a true interface
2. No need to know the details of the implementation. In fact hide them.
3. A static kind of interface
4. A bit like APIs

Related classes:
1. appconfignames.ConfigFactoryParamNames (Constants in the config file)
2. factoryinterface.IFactory (Core interface that is replicated here)
3. tests/apptests/test_factory.py (Sample test cases)
4. tests/apptests/data/test_factory_config.toml (Sample config file for a variety of class intantiations)

Documentation:
1. /factory.md
    Core concepts and motivation
    Describes the usage of the factory object
    Examples of how to use the factory object

"""
from aspire_tinyapp.appwall.appobjectsinterface import AppObjects
from aspire_tinyapp.interfaces.factoryinterface import IFactory
from typing import Any

"""
*************************************************
* Initialize the global factory object
*************************************************
"""

def _fact() -> IFactory:
    return AppObjects.getFact()

# This won't work because the factory object is not initialized
# so it has to be a method invocation
# use _fact() instead
#global_factory: IFactory  = _getGlobalFactory()


"""
*************************************************
* Standalone functions for IFactory methods
*************************************************
"""
# Assumes objects are anchored directly at the identifier
# throws an exception if the object is not found
def getObjectAbsolute(identifier: str, args: Any) -> Any:
    return _fact().getObjectAbsolute(identifier, args)

# Assumes objects are anchored at "request.name" where name is the object identifier below
# throws an exception if the object is not found
def getObject(identifier: str, args: Any) -> Any:
    return _fact().getObject(identifier, args)

# Exception versions of the same methods
def getObjectWithDefault(identifier: str, args: Any, defaultObject: Any) -> Any:
    return _fact().getObjectWithDefault(identifier, args, defaultObject)

def getObjectAbsoluteWithDefault(identifier: str, args: Any, defaultObject: Any) -> Any:
    return _fact().getObjectAbsoluteWithDefault(identifier, args, defaultObject)

"""
*************************************************
* Interpreted functions for IFactory methods
*************************************************
tbd
"""