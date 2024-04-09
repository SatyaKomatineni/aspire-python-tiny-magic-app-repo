# About Univesal Factory
Documents how objects are instantiated using the universal factory based on configuration

<!--*******************************************************-->
# Types of classes
<!--*******************************************************-->
This factility can be used to work with the following types of classes.

1. Singletons
2. Multiinstance classes
3. Executors (classes that return other objects like data or other classes)
4. Data classes: COnfigurations as objects
5. Dependency Injection

# Known Type of classes not covered
1. Classes with constructors with variable args and kwargs

<!--*******************************************************-->
# Note on imports to use this facility
<!--*******************************************************-->
I want you to read the usage story first.
I will cover the imports needed at the end of the article.

<!--*******************************************************-->
# Singleton example
<!--*******************************************************-->

Consider the following in a toml file

```
[testclasses_class1]
classname="apptests.test_factory_classes.TestSingletonClassNoConstructor"
```

Then you can instantiate any class indicated by the configuration root path ```testclasses_class1``` using the following code

```python
def _test1():
    obj = factory.getObjectAbsolute("testclasses_class1", None)
    log.prettyPrintObject(obj)
```

Here is what the class ```TestSingletonClassNoConstructor``` looks like

```python
class TestSingletonClassNoConstructor(ISingleton):
    def __init__(self):
        self.name = "TestSingletonClass"
        log.info("TestSingletonClassNoConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass
```

Here are some takeaways

1. As you progress through code you can replace the implementations in the configuration file
2. Don't have to change the client source code
3. You can provide backward compaitbility
4. This class can also implement any other expected "typed" interfaces by the client (by inheriting those interfaces)
5. As it is "promising" to be a singleton in the code (by extending ISingleton), author of the class is aware that it must be thread safe and other singleton constraints
6. This facility acts as a virtual constructor

<!--*******************************************************-->
# Singleton example: Lets overload the class with a few init params
<!--*******************************************************-->

The following is an example where the class can have a constructor.

```python

class TestSingletonClassWithConstructor(ISingleton):
    def __init__(self, param1: str, param2: str):
        self.param1 = param1
        self.param2 = param2
        log.info("TestSingletonClassWithConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass
```

Lets see now how to instantiate this class by specifying it in the toml configuration file.

[testclasses_class2]
classname="apptests.test_factory_classes.TestSingletonClassWithConstructor"
param1="param1 value"
param2="param2 value"

Lets now get/instantiate the object and print its contents, note it is still a singleton class.

```python
def _test2():
    obj = factory.getObjectAbsolute("testclasses_class2", None)
    log.prettyPrintObject(obj)

def test_factory_class2(self):
    log.ph1("Testing factory class 2: TestSingletonClassWithConstructor")
    test_factory_classes._test2()
    log.info("End testing factory class 2")
```

This will print

```
info: Creating a singleton of type: apptests.test_factory_classes.TestSingletonClassWithConstructor
info: TestSingletonClassWithConstructor constructor called
trace: Returning object of type: apptests.test_factory_classes.TestSingletonClassWithConstructor

{'param1': 'param1 value', 'param2': 'param2 value'}

info: End testing factory class 2
```

<!--*******************************************************-->
# Multiinstance classes example: with Constructor
<!--*******************************************************-->

Only difference is the class will not extend the ISingleton.

```python
class TestMIClassWithConstructor():
    def __init__(self, param1: str, param2: str):
        self.param1 = param1
        self.param2 = param2
        log.info("TestMIClassWithConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test3():
    obj1 = factory.getObjectAbsolute("testclasses_class3", None)
    log.prettyPrintObject(obj1)

    obj2 = factory.getObjectAbsolute("testclasses_class3", None)
    log.prettyPrintObject(obj2)
```

This will print

```
Testing factory class 2: TestMIClassWithConstructor
***********************
info: Creating a non-singleton object of type: apptests.test_factory_classes.TestMIClassWithConstructor
info: TestMIClassWithConstructor constructor called
trace: Returning object of type: apptests.test_factory_classes.TestMIClassWithConstructor
{'param1': 'param1 value', 'param2': 'param2 value'}

# The second object

info: Creating a non-singleton object of type: apptests.test_factory_classes.TestMIClassWithConstructor
info: TestMIClassWithConstructor constructor called
trace: Returning object of type: apptests.test_factory_classes.TestMIClassWithConstructor
{'param1': 'param1 value', 'param2': 'param2 value'}
info: End testing factory class 2
```

Notice the debug information that points to the creation of the obect twice.

<!--*******************************************************-->
# Multiinstance classes example: with No Constructor
<!--*******************************************************-->
Very similar.

Nevertheless an example

```python
"""
*************************************************
* Test4, class4: TestMIClassNoConstructor
*************************************************
about:
1. No Constructor
2. Multi-instance

config entry:
[testclasses_class4]
classname="apptests.test_factory_classes.TestMIClassNoConstructor"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class4", None)
"""
class TestMIClassNoConstructor():
    def __init__(self):
        log.info("TestMIClassNoConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

def _test4():
    obj1 = factory.getObjectAbsolute("testclasses_class4", None)
    log.prettyPrintObject(obj1)

    obj2 = factory.getObjectAbsolute("testclasses_class4", None)
    log.prettyPrintObject(obj2)

```

The output looks like

```
Testing factory class 4: TestMIClassNoConstructor
***********************
info: Creating a non-singleton object of type: apptests.test_factory_classes.TestMIClassNoConstructor
info: TestMIClassNoConstructor constructor called
trace: Returning object of type: apptests.test_factory_classes.TestMIClassNoConstructor
{}

# Second object

info: Creating a non-singleton object of type: apptests.test_factory_classes.TestMIClassNoConstructor
info: TestMIClassNoConstructor constructor called
trace: Returning object of type: apptests.test_factory_classes.TestMIClassNoConstructor
{}
info: End testing factory class 4
```

<!--*******************************************************-->
# Making use of explicit initializers
<!--*******************************************************-->

In this approach classes can take advantage of the explicit configruration context in which they are invoked from.

Usually dependency injection takes care of setting the constructor arguments and hence the class doesn't need to be aware of the additional configuration.

If the class wants to be very selective about validation of these input variables during construction itself it can take advantage of a few interfaces to do do.

This can be done "along with" dependency injection if needed where an explicit init method can further validate the input arguments.

There are two interfaces that controls this behvior

```python
from aspire_tinyapp.interfaces.objectinterfaces import (
    IInitializable, 
    IInitializableWithArgs)
```

Lets look at each one now.

<!--*******************************************************-->
# Classes that want explicit "pull" initialization from configuration files
<!--*******************************************************-->
These classes can be both Singletons or multi-instance.

Initialization is gurantted to take place after the class is contructed.

Classes can have constructors or no constructors.

Dependency injection is used to call constructors.

Once the object is constructed it is initialazed explicitly by passing the configuration root string where this class is anchored.

If the class is a singleton, this initialization is called ONLY ONCE. 

If the class is a multi-instance the initializaiton is called after each instance creation.

