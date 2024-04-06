
from aspire_tinyapp.baselib import baselog as log

from src.aspire_tinyapp.interfaces.objectinterfaces import (
    ISingleton, 
    IInitializable, 
    IInitializableWithArgs,
    IExecutor)


"""
*************************************************
* Harness class
*************************************************
"""
import unittest
from aspire_tinyapp.baselib import baselog as log
from aspire_tinyapp.appwall.appinitializer import AppInitializer
from aspire_tinyapp.appwall.appobjectsinterface import AppObjects
from aspire_tinyapp.baselib import fileutils as fileutils
from aspire_tinyapp.interfaces.configinterface import IDictionaryConfig

from apptests import test_factory_classes as test_factory_classes

from typing import Any

def _getConfigFilename() -> str:
    curdir = fileutils.getCurrentFileRoot(__file__)
    tomlConfigFilename = fileutils.pathjoin_segments(curdir, "data", "test_factory_config.toml")
    return tomlConfigFilename


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        log.ph("Setting up the test environment", "start")
        configfilename = _getConfigFilename()
        AppInitializer.initializeApplication(configfilename)
        log.ph1("Printing Dictionary for debugging")
        AppObjects.printConfig()
        log.ph1("Test setup complete. Real tests start.")

    @classmethod
    def tearDownClass(cls):
        log.ph("Stopping the tests", "done")

    def test_hello(self):
        log.info("hello method")

    def test_simpleObject(self):
        log.info("Testing simple object")
        fact = AppObjects.getFact()
        testclassObj = fact.getObjectAbsolute("testclass", None)
        log.prettyPrintObject(testclassObj)

    def test_Executor(self):
        log.info("Testing Executor object")
        fact = AppObjects.getFact()
        reply = fact.getObject("readdata", None)
        log.info(f"Reply from readdata transaction: {reply}")

    def test_Executor_di(self):
        log.info("Testing DI Executor object")
        fact = AppObjects.getFact()
        reply = fact.getObject("readdata_di", None)
        log.info(f"Reply from readdata DI transaction: {reply}")

    def test_factory_class1(self):
        log.ph1("Testing factory class1")
        test_factory_classes._test1()
        log.info("End testing factory class1")

    def test_factory_class2(self):
        log.ph1("Testing factory class 2")
        test_factory_classes._test2()
        log.info("End testing factory class 2")

"""
*************************************************
* End: Harness class
*************************************************
"""

"""
*************************************************
* Test IExecutor
*************************************************
[request.readdata]
classname="apptests.test_factory.HelloWorldReader"
text="Hello world"
"""

class HelloWorldReader(IExecutor):
    def execute(self, config_root_context: str, args: Any) -> Any:
        cfg = AppObjects.getConfig()
        text = cfg.getValue(config_root_context + ".text")
        return text

class HelloWorldReaderDI(IExecutor):
    def __init__(self, text: str):
        self.text = text

    def execute(self, config_root_context: str, args: Any) -> Any:
        return self.text

"""
*************************************************
* Test IInitializable, Singleton: TestClass
*************************************************
"""
class TestClass(ISingleton, IInitializable):
    rootContext: str
    def initialize(self, rootContext: str) -> None:
        log.info("Initializing the class TestClass")
        self.rootContext = rootContext

def _test1():
    obj = TestClass()
    obj.initialize("Root Context")
    log.prettyPrintObject(obj)

"""
*************************************************
* Testing start
*************************************************
"""

def test():
    unittest.main()
    #_test1()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()