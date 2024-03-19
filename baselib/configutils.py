"""
*************************************************
* File specific imports
*************************************************
"""
import tomlkit
from typing import Any
import json
from flatten_dict import flatten #type:ignore

"""
*************************************************
* other libs
*************************************************
"""
from baselib import baselog as log
from baselib import fileutils as fileutils

"""
Given a toml configuration filename returna  flattened dictionary.
Public method.
"""
def getTOML_flattened_dictionary(tomlConfigFilename: str)-> dict[str, Any]:
    return _getFlattenedDictionary(tomlConfigFilename)

"""
*************************************************
* Datetime json support
*************************************************
"""
from datetime import datetime, date, time
from typing import Any, Dict

class TypedDateTimeEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Dict[str, Any]:
        if isinstance(o, datetime):
            return {"type": "datetime", "value": o.isoformat()}
        elif isinstance(o, date):
            return {"type": "date", "value": o.isoformat()}
        elif isinstance(o, time):
            return {"type": "time", "value": o.isoformat()}
        return super().default(o)
    

def typed_datetime_decoder(dct: Dict[str, Any]) -> Any:
    if "type" in dct and "value" in dct:
        type_info = dct["type"]
        value = dct["value"]
        if type_info == "datetime":
            return datetime.fromisoformat(value)
        elif type_info == "date":
            return date.fromisoformat(value)
        elif type_info == "time":
            return time.fromisoformat(value)
    return dct  # Return the original dictionary if no type info is found
   

"""
*************************************************
* End: json support
*************************************************
"""
"""
Given a toml configuration filename returna  flattened dictionary
"""
def _getFlattenedDictionary(tomlConfigFilename: str) -> dict[str, Any]:
    log.ph("Reading TOML configuration file", tomlConfigFilename)
    # Read and parse the toml file
    toml_str = fileutils.read_text_file(tomlConfigFilename)
    parsed_toml: tomlkit.TOMLDocument = tomlkit.parse(toml_str)
    # convert it to json
    json_str: str = json.dumps(parsed_toml,indent=4, cls=TypedDateTimeEncoder)
    dict = json.loads(json_str, object_hook=typed_datetime_decoder)
    flat_dict = flatten(dict, reducer="dot") #type:ignore
    new_dict = _process_dict_for_aliases(flat_dict) #type:ignore
    return new_dict #type:ignore

def _process_dict_for_aliases(input_dict: dict[str,Any]) -> dict[str,Any]:
    log.info("Resolving aliases in the config file")
    # Create a copy of the dictionary to modify and return
    modified_dict = input_dict.copy()
    
    for key, value in input_dict.items():
        # Check if the value is a string and starts with "a@"
        if isinstance(value, str) and value.startswith("a@"):
            # Extract the rest of the value after "a@"
            new_key = value[2:]
            # Check if the extracted value is a key in the original dictionary
            if new_key in input_dict:
                # Replace the current value with the looked up value
                modified_dict[key] = input_dict[new_key]
            else:
                # If the new_key is not found, raise an exception
                raise ValueError(f"Aliased key '{new_key}' not found.")
    
    return modified_dict
"""
*************************************************
* Get sample configuration filename
*************************************************
"""
def _getSampleConfigFile() -> str:
    root = fileutils.getDataRoot()
    return fileutils.pathjoin(root, "appconfig.toml")

def _printConfigFilename():
    r = _getSampleConfigFile()
    log.ph("Config file", r)

def test():
    _printConfigFilename()
    d = _getFlattenedDictionary(_getSampleConfigFile())
    log.ph("Flattened dict", d)

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()