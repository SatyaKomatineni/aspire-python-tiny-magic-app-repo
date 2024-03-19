
from baselib import baselog as log

from baselib.objectinterfaces import (
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
from baselib import baselog as log
from appwall.appinitializer import AppInitializer
from appwall.appobjectsinterface import AppObjects
from baselib import fileutils as fileutils
from baselib.configinterface import IDictionaryConfig
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