# About Factory.md
Documents how objects are instantiated using the universal factory based on configuration

# Type of classes
1. Singletons
2. Multiinstance classes
3. Executors (classes that return other objects like data or other classes)
4. Data classes: COnfigurations as objects
5. Dependency Injection

# Known Type of classes not covered
1. Constructors with variable args and kwargs

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
4. This class can implement any other expected interfaces by the client
5. As it is promising to be a singleton in the code, the author of the class is aware that it must be thread safe and other constraints
6. Acts as a virtual constructor

<!--*******************************************************-->
# Singleton example: Lets overload the class with a few init params
<!--*******************************************************-->

class TestSingletonClassWithConstructor(ISingleton):
    def __init__(self, param1: str, param2: str):
        self.param1 = param1
        self.param2 = param2
        log.info("TestSingletonClassWithConstructor constructor called")

    def _someMethod(self):
        log.info("Some method called")
        pass

Lets see now how to instantiate this class by specifying it in the toml configuration file.

[testclasses_class2]
classname="apptests.test_factory_classes.TestSingletonClassWithConstructor"
param1="param1 value"
param2="param2 value"

Lets now get the object and print its contents, note it is still a singleton class
