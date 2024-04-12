# About Universal Factory
Documents how objects are instantiated using a ```universal factory```, based on configuration.

This is part of a python module that simulates what a tiny application is:

**[asspire_tinyapp](./README.md)**

```python
pip install aspire_tinyapp
```

coming soon.

You ask why, lets take an example:

<!--*******************************************************-->
# Singleton example
<!--*******************************************************-->

Consider the following in a toml configuration file

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

Why is this useful?

Here are some takeaways

1. As you progress through code you can replace the implementations in the configuration file as long as it adheres to the implementation (it is even more general than that. you will see)
2. Don't have to change the client source code
3. You can provide backward compaitbility
4. This class can also implement any other expected "typed" interfaces by the client (by inheriting those interfaces)
5. As it is "promising" to be a singleton in the code (by extending ISingleton), author of the class is aware that it must be thread safe and other singleton constraints. This it enforces singletons
6. This facility acts as a virtual constructor

<!--*******************************************************-->
# Types of classes
<!--*******************************************************-->
This factility can be used to work with the following types of classes.

1. Singletons
2. Multiinstance classes
3. Executors (classes that return other objects like data or other classes)
4. Data classes: COnfigurations as objects
5. Dependency Injected classes

# Known Type of classes that are not covered
1. Classes with constructors with variable args and kwargs

<!--*******************************************************-->
# Note on imports to use this facility
<!--*******************************************************-->
I want you to read the usage story first.

```python
from aspire_tinyapp.publicinterfaces import factory
from aspire_tinyapp.publicinterfaces import config
from aspire_tinyapp.baselib import baselog as log

```

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

**Once the object is constructed it is initialazed explicitly by passing the configuration root string where this class is anchored.**

If the class is a singleton, this initialization is called ONLY ONCE. 

If the class is a multi-instance the initializaiton is called after each instance creation.

<!--*******************************************************-->
# Using the IInitiaization interface
<!--*******************************************************-->
Consider the following configuration for a class

```
[testclasses_class5]
classname="apptests.test_factory_classes.TestClassWithInitializer"
param1="param1 value"
param2="param2 value"
```

Lets look the class definition now

```python
"""
*************************************************
* Test5, class5: TestClassWithInitializer
*************************************************
about:
1. No Constructor
2. Singleton
3. Initializable
"""
class TestClassWithInitializer(ISingleton, IInitializable):
    # Variable to hold the root context in the configruation file
    # in this case it will point to "testclasses_class5"
    contextRoot: str

    # you can then use to read the following
    param1: str
    param2: str

    def __init__(self):
        self.name = "TestClassWithInitializer"
        log.info("TestClassWithInitializer constructor called")

    # implementing the IInitializable interface
    def initialize(self, rootContext: str) -> None:
        self.contextRoot = rootContext
        self.param1 = config.getValue(rootContext + ".param1")
        self.param2 = config.getValue(rootContext + ".param2")

    def _someMethod(self):
        log.info("Some method called")
        pass
```

Call to the initialize method gives explicit control on initialization aspects of the class. 

In this case this class happens to be a singleton, but will also work the same way for multi-instance.

Here is how this class is invoked

```python
def _test5():
    obj = factory.getObjectAbsolute("testclasses_class5", None)
    log.prettyPrintObject(obj)
```

This will print the following

```
info: Creating a singleton of type: apptests.test_factory_classes.TestClassWithInitializer
info: TestClassWithInitializer constructor called
trace: Returning object of type: apptests.test_factory_classes.TestClassWithInitializer
{   'contextRoot': 'testclasses_class5',
    'name': 'TestClassWithInitializer',
    'param1': 'param1 value',
    'param2': 'param2 value'}
```

<!--*******************************************************-->
# A Multi-instance class as a function (IExecutor)
<!--*******************************************************-->

Consider the following in configuration file

```python
[testclasses_class7]
classname="apptests.test_factory_classes.TestClassMIECWithInitializerArgs"
param1="param1 value"
param2="Send back hello world via execute method"
```

Goal here is to initialize the class with the parameters from the configuration file and then call its execute method.

Whatever object or interface or data that execute method returns is returned back to the caller.

In this example the execute method will return the "param2" back to the caller.

Let's see how this works, simply.

Here is a class with all bells and whistles

```python
"""
*************************************************
* Test 7, class 7: TestClassMIECWithInitializerArgs
*************************************************
about:
1. Explicit Constructor (C)
2. Multi Instance (MI)
3. Executor (E)
3. InitializableWithArgs

config entry:
[testclasses_class7]
classname="apptests.test_factory_classes.TestClassMIECWithInitializerArgs"
param1="param1 value"
param2="Send back hello world via execute method"

#how to get it
obj = factory.getObjectAbsolute("testclasses_class7", None)
"""
class TestClassMIECWithInitializerArgs(IExecutor, IInitializableWithArgs):
    # Variable to hold the root context in the configruation file
    # in this case it will point to "testclasses_class5"
    contextRoot: str

    # you can then use to read the following
    param1: str
    param2: str
    param3_from_args: str

    def __init__(self, param1: str, param2: str):
        self.name = "TestClassMIECWithInitializerArgs"
        log.info("TestClassMIECWithInitializerArgs constructor called")
        self.param1 = param1
        self.param2 = param2

    # implementing the IInitializable interface
    def initializeWithArgs(self, rootContext: str, args: str) -> None:
        self.contextRoot = rootContext

        # this is the additional parameter that is passed in the args
        self.param3_from_args = args

    # Implementing the IExecutor interface
    def execute(self, config_root_context: str, args: Any) -> Any:
        return self.param2

    def _someMethod(self):
        log.info("Some method called")
        pass

```

**Note: This code will also work if the class is not implementign the IInitializableWithArgs as well.**

That option gives an additional avenue for the factory to pass additional args from code and not merely configuration.

Here is how to get back the output 

```python
def _test7():
    obj = factory.getObjectAbsolute("testclasses_class7", "Third argument value")
    log.info(f"Returned value from execute: {obj}")
```

Notice how what is returned is the output of the IExecutor.

The output will be

```
info: Creating a non-singleton object of type: apptests.test_factory_classes.TestClassMIECWithInitializerArgs
info: TestClassMIECWithInitializerArgs constructor called
trace: Returning object of type: apptests.test_factory_classes.TestClassMIECWithInitializerArgs
info: Returned value from execute: Send back hello world via execute method
```

<!--*******************************************************-->
# Current limitations with SIE (Single Instance Executors)
<!--*******************************************************-->

Take the followign example

```
[request.readdata]
classname="apptests.test_factory.HelloWorldReader"
text="Hello world"
```

And now consider the class ```HellowWorldRerader```

```python
class HelloWorldReader(IExecutor):
    def execute(self, config_root_context: str, args: Any) -> Any:
        text = config.getValue(config_root_context + ".text")
        return text
```

The way you invoke it is

```python
result = factory.getObject("readdata", None)
assertEqual(result, "Hello World")
```

Few things to notice here

1. Notice how the ```HelloWorldReader``` is not a Singleton.
2. The factory works in such a way that it instantiates the object of type ```HelloWorldReader```
3. Note, it does not return that object as a factory usually does
4. instead it returns the "output" of the execute method (a level of indirection)
5. factory decides on this behavior only if the class implements "IExecutor"

Now, this makes sense when the class is an MI (Multi-instance).

This poses some problems when the class is an "SI" (Single Instance).

Take the following examples

```
[request.readfile1]
classname = some_pkg.FileReader
filename = some-path-1

[request.readfile2]
classname = some_pkg.FileReader
filename = some-path-2
```

Although FileReader can be an MI, you can also imagine it to be an SI.

It is conceivable that the FileReader first has to be constructed. It may need its own initialization parameters.

if it is constructed only once, being an SI, where do those config params go? With request1 or request2, or both?

**As a result it makes more sense for executors to be MI.**

However you can still use an SI for this, under the following circumstances

1. You find that being an SI is SIGNIFICANTLY better in resources or time
2. That it has a default constructor with no args
3. If it needs args, the default constructor indirectly gets them via config from another single set with it own one time definition of that configuration

**A future enhancement of the factory could be that it allows for that "one time" configuration for a (Singleton) class when it is specified in multiple entries in a config file.**

<!--*******************************************************-->
# Data classes: Classes to hold some configuration in a concise type safe manner
<!--*******************************************************-->

Consider the following data class

```python
@dataclass
class TestDataClass:
    param_str: str
    param_int_1: int
    param_float: float
    param_bool: bool
    param_list: list[int]
```

Consider a configuration entry like this

```python
[testclasses_class8]
classname="apptests.test_factory_classes.TestDataClass"
param_str="string value"
param_int_1=5
param_float=5.6
param_bool=true
param_list=[1,2,3]
```

In your python code you can do access these configuration parameters as a data object

```python
obj = factory.getObjectAbsolute("testclasses_class8", None)
print(obj.param_bool obj.param_list)
etc.
```

By declaring the TestDataClass as a ```@dataclass``` python does a few things for the class. 

These items are:

1. Auto generates the init method, repr, eq etc.
2. Allows to declares variables nicely based on their types 
3. A simple syntax for default values
4. Calls post init if needed
5. Further field decorators (Read up on this)
6. Can be made immutable (Read up on this)

Be careful however the syntax of a data class is slightly different from non data class. Especially in declaring defaults. A default value this way with out a data class will make that a class variable and not an  instance variable.

<!--*******************************************************-->
# Few notes on toml config files
<!--*******************************************************-->

Consider the following configuration in a toml file

```python
[testclasses_class8]
classname="apptests.test_factory_classes.TestDataClass"
param_str="string value"
param_int_1=5
param_float=5.6
param_bool=true
param_list=[1,2,3]

```

Here are some notes

1. Toml distinquishes types in the values of keys
2. Allowed types include strings, integers, date, time, datetime, and even lists
3. However it does not allow dictionaries as values

This means data classes that have dictionaries as fields do not work at this time.

Toml does allow so called "inline" tables or dictionaries. Here is how they look

```python
[testclasses_class8]
classname="apptests.test_factory_classes.TestDataClass"
param_bool=true
param_list=[1,2,3]
param_dict={key1="b", key2=5}
```

In this case the syntax is not a default python dictionary syntax.

Internally it is represented as a dictionary against "param_dict", but the current implementation of this configuration "flattens" dictionaries resulting in the following equivalent structure

```python
[testclasses_class8]
classname="apptests.test_factory_classes.TestDataClass"
param_dict.key1="b"
param_dict.key2=5
```

and there by lossing their dictionary identity.

There are a couple of ways to tackle this.

But for now dictionaries are not automatically digested via dependency injection.

Inseady you can, if necessary, handle this in a couple of ways:

1. Directly with an initializer and reading the config values yourself
2. Or represent the dictionary in a string with escape chracters and parse the string yourself in your init code

**In the future I will see how much this is needed, and how best to handle**

<!--*******************************************************-->
# Common Errors
<!--*******************************************************-->

1. Ignoring "self" in instance methods
2. init methods not taking "self"
2. Ignoring "self" in setting instance variables
3. Using wrong abstract method signatures (or names) when extending object interfaces like ISingleton, IInitializable, IInitializableWithArgs, IExecutor etc. This will result in class construction failure as Python thinks the classes are still abstract.

<!--*******************************************************-->
# Important design considerations
<!--*******************************************************-->
1. The objects are stored in the singleton cache based on "fqcn" (fully qualified class name)
2. So, know that uniqueness is NOT based on the string in the configuration file for that object but its fqcn
