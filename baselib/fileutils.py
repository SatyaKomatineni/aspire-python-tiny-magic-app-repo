
from baselib import baselog as log
import os
import pickle
from pathlib import Path
import baselib
from typing import Any

"""
***********************************
Static directories functions
***********************************
"""
def getProjectRoot():
    return _getProjectRoot()

def getDataRoot():
    return pathjoin(getProjectRoot(), "data")    

def getDatasetRoot():
    return os.path.join(getDataRoot(),"datasets")

def getSonnetsRoot():
    return os.path.join(getDatasetRoot(), "sonnets")


def pathjoin(seg1: str, path: str):
    return os.path.join(seg1,path)

def pathjoin_segments(seg1: str, *pathSegments: str):
    return os.path.join(seg1, *pathSegments)

def getTempDataRoot():
    return os.path.join(getDataRoot(),"tempdata")

def _getProjectRoot() -> str:
    baselibPath = Path(baselib.__file__)
    parent = baselibPath.parent.parent.resolve()
    return str(parent)

"""
Returns the parent directory where this file is residing
param: current_file_ref: use the __file__ where you are calling this function
"""
def getCurrentFileRoot(current_file_ref: str) -> str:
    path = Path(current_file_ref)
    return str(path.parent)


"""
***********************************
writing to files
***********************************
"""
def save_text_to_file(text: str, filename: str):
    """
    Saves the given text to a file.

    Args:
    text (str): The text to save.
    filename (str): The name of the file to save the text to.

    Returns:
    None
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def testSaveToFile():
    text_to_save = "Hello, this is a sample text."
    filename = "./temp/sample.txt"
    save_text_to_file(text_to_save, filename)

"""
***********************************
Reading from files
***********************************
"""
def read_text_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    return file_contents


"""
***********************************
General utilities
***********************************
"""
def getEnvVariable(name: str, default: str):
    value = os.environ[name] 
    if log.isEmptyString(value):
        return default
    return value

def exists(fullfilePath: str):
    return os.path.exists(fullfilePath)

"""
*************************************************
* Object state
*************************************************
"""
def getTempDataFilename(filename: str):
    tempDataRoot = getTempDataRoot()
    return pathjoin(tempDataRoot, filename)

def store_object_to_file(obj: Any, filename: str):
    filepath = getTempDataFilename(filename)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)
    return filepath

def read_object_from_file(filename: str):
    filepath = getTempDataFilename(filename)
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    return obj


def localTest():
    log.ph1("Starting local test")
    log.dprint(getTempDataRoot())
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
