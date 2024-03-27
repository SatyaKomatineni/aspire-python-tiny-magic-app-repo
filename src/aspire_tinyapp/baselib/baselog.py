"""
#**********************************************
Module Name: baselog

Description: 
1. To provide pretty print statements
2. Allow for h1, h2, h3 etc
3. Possibly provide time stamps

Usage:
1. Just see the functions

#Date: 1/20/24
#**********************************************
"""
import regex as re
from typing import Any
import pprint   

"""
#**********************************************
Backlog:
1. Provide levels to debug to better control print statements
2. Provide a enum with print statements (info, debug, trace, etc)
#**********************************************
"""
#**********************************************
# Define module-level variables and constants here
#**********************************************
#None

#**********************************************
# Functions
#**********************************************

pp = pprint.PrettyPrinter(indent=4)

global_debug = True

def turnOffDebug():
    global global_debug
    global_debug = False

    
def dprint(text: str):
    if global_debug == False :
        return
    print(text)

def p(text: str):
    dprint(f"{text}")

def ph(h: str,m: object):
    dprint(f"\n{h}")
    dprint("***********************")
    dprint(f"{m}")

def ptype(context: str, o: object):
    dprint(f"Type of {context}:\n{type(o)}")

def uph1(h: str):
    print(f"\n{h}")
    print("***********************")

def uph(h: str,m: object):
    print(f"\n{h}")
    print("***********************")
    print(f"{m}")

def ph1(h: str):
    dprint(f"\n{h}")
    dprint("***********************")

def prompt(text: str) -> str:
    return input(f"\n> {text}")

#**********************************************
# log classification
#**********************************************
def warn(m: str):
    dprint(f"warn: {m}")

def trace(m: str):
    dprint(f"trace: {m}")
    
def info(m: str):
    dprint(f"info: {m}")

"""
*************************************************
* Log exception
*************************************************
"""
def logException(msg: str, e: Exception):
    ph(msg, str(e))



#**********************************************
# Validation functions
#**********************************************

def validate_not_null_or_empty(context: str, *args: Any):
    for arg in args:
        if arg is None:
            raise ValueError(f"The specified Argument {arg} cannot be null or empty.\nContext: {context}")
        elif isinstance(arg, str) and not arg.strip():
            raise ValueError(f"The specified Argument {arg} cannot be an empty string\nContext: {context}")


def examine_large_string(text: str, max_length: int, context: str):
    ph1(f"Examining a large string: {context}")
    if isEmptyString(text):
        dprint("The input string is empty.")
        return
    dprint("It is a valid string")
    dprint(f"Size of the string: {len(text)} characters")
    dprint(f"\n{text[:max_length]}")

def isValidString(s: str):
    return bool(s and not s.isspace())

def isEmptyString(s: str):
    return not isValidString(s)

from typing import Any, Type

def assertType(object: Any, typename: Type[Any], message: str) -> None:
    """
    Asserts that the given object is of the specified type.
    Example: assertType("hello", str, "Has to be a string")

    :param object: The object to check the type of.
    :param typename: The type the object is expected to be.
    :param message: The message to include in the exception if the check fails.
    :raises TypeError: If the object is not of the expected type.
    """
    if not isinstance(object, typename):
        raise TypeError(f"{message}. Expected type: {typename.__name__}, got: {type(object).__name__}")



#**********************************************
# End: Validation functions
#**********************************************
    
#**********************************************
# Utility functions
#**********************************************
def is_roman_numeral(s: str):
    # Regular expression pattern for Roman numerals
    pattern = r'^[IVXLCDM]+$'

    # Match the pattern with the string
    if re.match(pattern, s):
        return True
    else:
        return False
    
def summarizeDictionary(d: dict[Any, Any]):
    ph1("Summarizing a dictionary")
    size = len(d)
    if size == 0:
        dprint("It is an empty dictionary")
        return
    dprint(f"Size: {len(d)}")
    dprint(f"Printing first row")
    pair = next(enumerate(d.items()))
    dprint(f"{pair[1]}")

def summarizeLargeText(large_text: str):
    validate_not_null_or_empty(large_text)
    dprint(large_text[:200])
    
def testSummarizeDictionary():
    d = {1:"1", 2:"2"}
    summarizeDictionary(d)

def prettyPrintDictionary(d: dict[Any,Any]):
    pp.pprint(d)

def prettyPrintObject(o: Any):
    pp.pprint(o.__dict__)
    
#**********************************************
# Utility functions
#**********************************************

def _testStrings():
    ph1("Testing strings")
    info(f"{isEmptyString('ddd')}")
    info(f"{isValidString('ddd')}")
    info(f"{isValidString('')}")
    info(f"{isValidString('   ')}")

def localTest():
    ph1("Starting local test")
    testSummarizeDictionary()
    _testStrings()
    print ("End local test")

if __name__ == '__main__':
    localTest()