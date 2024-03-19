"""
*************************************************
* Test Configuration
*************************************************
data files used:
/data/testconfig.toml

Code:
1. write me a unit test class TestConfig
2. Provide methods to setup and tear down at the class level
3. Create 1 test to start with called "test1_simpleConfig()"

"""

import unittest
from baselib import baselog as log
from appwall.appinitializer import AppInitializer
from appwall.appobjectsinterface import AppObjects
from baselib import fileutils as fileutils
from baselib.configinterface import IDictionaryConfig
from datetime import  date
from datetime import  datetime
from datetime import  time


def _getConfigFilename() -> str:
    curdir = fileutils.getCurrentFileRoot(__file__)
    tomlConfigFilename = fileutils.pathjoin_segments(curdir, "data", "testconfig1.toml")
    return tomlConfigFilename


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        log.ph("Setting up the test environment", "start")
        configfilename = _getConfigFilename()
        AppInitializer.initializeApplication(configfilename)
        log.ph1("Printing Dictionary for debugging")
        _printConfig()
        log.ph1("Test setup complete. Real tests start.")

    @classmethod
    def tearDownClass(cls):
        log.ph("Stopping the tests", "done")

    """
    *************************************************
    * getValue(): Testing direct key at root
    *************************************************
    """
    def test1_getValueExisting(self):
        cfg = AppObjects.getConfig()

        # Test direct key at root level
        log.info("Testing direct key at root")
        value = cfg.getValue("key1")
        self.assertEqual(value, "key1")

        # Test a sub key under a category
        log.info("Testing a sub key: topic1.key1")
        value = cfg.getValue("topic1.key1")
        self.assertEqual(value, "topic1 key1")


    """
    *************************************************
    * getValue(): Testing a non existent key for exception
    *************************************************
    """
    def test1_getValueNonExisting(self):
        cfg = AppObjects.getConfig()
        log.info("Testing a non existent key for exception")
        with self.assertRaises(Exception):
            cfg.getValue("Non-existent-key")

    """
    *************************************************
    * getValue(): Test aliases
    *************************************************
    """
    def test1_getValueAliasedValue(self):
        cfg = AppObjects.getConfig()
        log.info("Testing for an aliased value")
        value = cfg.getValue("topic2.aliasedkey")
        self.assertEqual(value,"key1")

    """
    *************************************************
    * getValueAsObject(): Test integer values
    *************************************************
    [intvalues]
    five=5
    decimal=5.3
    """
    def test1_getValueAsObjectInt(self):
        cfg = AppObjects.getConfig()
        log.info("Testing for integer values")

        #As a string
        value_str = cfg.getValue("intvalues.five")
        self.assertEqual(value_str, "5")

        value_int = cfg.getValueAsObject("intvalues.five")
        self.assertEqual(value_int, 5)

        value_int = cfg.getValueAsObject("intvalues.decimal")
        self.assertEqual(value_int, 5.3)

    """
    *************************************************
    * getValueAsObject(): Test dates
    *************************************************
    [datetimes]
    date = 2024-03-17
    datetime1 = 2024-03-17T10:00:00
    datetime2 = 2024-03-17T14:00:00
    time=9:00:00

    """

    def dbg_test1_getValueAsObjectDatetime(self):
        cfg = AppObjects.getConfig()
        log.info("Testing for datetime values")

        value = cfg.getValue("datetimes.date")
        date_object = date(2024, 3, 17)
        self.assertEqual(value,date_object)

        value = cfg.getValue("datetimes.datetime1")
        datetime1_object = datetime(2024, 3, 17, 10, 0, 0)
        self.assertEqual(value,datetime1_object)

        value = cfg.getValue("datetimes.datetime2")
        datetime2_object = datetime(2024, 3, 17, 14, 0, 0)
        self.assertEqual(value,datetime2_object)

        value = cfg.getValue("datetimes.time")
        time_object = time(9,0,0)
        self.assertEqual(value,time_object)

    def test1_getValueAsObjectDatetime(self):
        cfg = AppObjects.getConfig()
        log.info("Testing for datetime values")

        value = cfg.getValueAsObject("datetimes.date")
        log.info(value)
        value = cfg.getValueAsObject("datetimes.datetime1")
        log.info(value)
        value = cfg.getValueAsObject("datetimes.datetime2")
        log.info(value)
        value = cfg.getValueAsObject("datetimes.time")
        log.info(value)

    """
    *************************************************
    * list values
    *************************************************
    [lists]
    numberlist=[1,2,34]
    """    
    def test1_getValueAsObjectLists(self):
        cfg = AppObjects.getConfig()
        log.info("Testing for list values")

        value = cfg.getValueAsObject("lists.numberlist")
        targetList = [1,2,34]
        self.assertListEqual(value,targetList)
"""
*************************************************
* End of class: unittest
*************************************************
"""    

def _printConfig():
    cfg = AppObjects.getConfig()
    if isinstance(cfg, IDictionaryConfig):
        d = cfg.getKeyValuesAsDictionary()
        log.prettyPrintDictionary(d)

def test():
    unittest.main()
    #log.ph("Configuration filename", _getConfigFilename())

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
