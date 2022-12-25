import json

import pandas as pd
import yaml
from pandas import DataFrame
from yaml import SafeLoader

from model import MailTemplateModel


def parse_data_file_to_send_items(data_path: str):
    data_: DataFrame = pd.read_excel(data_path, sheet_name=0, header=0, converters={"agent_code": str})

    json_str = data_.to_json()
    if json_str is None:
        raise ValueError("Cannot read data from excel file")

    json_data_ = json.loads(json_str)
    data_length_ = len(data_)

    result_: list[dict[str, str | None]] = []

    for idx_ in range(0, data_length_):
        item_: dict[str, str | None] = dict()

        for key_ in data_.keys():
            value_ = json_data_[key_][str(idx_)]
            item_[key_] = None if value_ is None else str(value_)

        result_.append(item_)

    return result_


def read_mail_template(template_path: str):
    return MailTemplateModel.from_file(template_path)


def read_setting():
    with open("../settings.yml", encoding='utf-8') as f_:
        return yaml.load(f_, Loader=SafeLoader)
