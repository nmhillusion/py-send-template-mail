from datetime import date
from typing import Callable


def mapping_key_to_func(key_name_: str):
    if "str" == key_name_:
        return str
    if "int" == key_name_:
        return int
    if "None" == key_name_:
        return lambda: None
    return None


def mapping_config_to_func(config_: dict[str, list[str]]):
    converters_: dict[str, Callable] = {}
    for type_ in config_:
        columns_of_type_ = config_[type_]

        if columns_of_type_ is not None:
            for col_name_ in columns_of_type_:
                converter_ = mapping_key_to_func(type_)
                if converter_ is not None:
                    converters_[col_name_] = converter_

    return converters_
