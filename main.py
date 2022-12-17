import json

import pandas as pd
import yaml
from pandas import DataFrame
from yaml import SafeLoader

from engine import MailSender
from engine import MailTemplateBuilder
from model import MailTemplateModel


def parse_data_file_to_send_items(data_path: str):
    data_: DataFrame = pd.read_excel(data_path, sheet_name=0, header=0, converters={"agent_code": str})

    json_str = data_.to_json()
    if json_str is None:
        raise Exception("Cannot read data from excel file")

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
    with open("./settings.yml", encoding='utf-8') as f_:
        return yaml.load(f_, Loader=SafeLoader)


######################################################
# MAIN PROGRAM #######################################
######################################################


def run():
    settings = read_setting()
    mail_template_: MailTemplateModel = read_mail_template(settings["path"]["template"])
    mail_builder_ = MailTemplateBuilder(mail_template_)

    send_items_ = parse_data_file_to_send_items(settings["path"]["data"])

    result_ = {"success": 0, "failure": []}
    for si_ in send_items_:
        try:
            MailSender(mail_model=mail_builder_.build(si_), send_item=si_).send_mail()

            result_["success"] += 1
        except Exception as ex:
            print(f"ERROR: {ex}")
            result_["failure"].append(ex)

    print(f"==== Running results ===========")
    print(f"\tSuccess: {result_['success']}")
    print(f"\tFailure: {len(result_['failure'])}")
    if 0 < len(result_["failure"]):
        print(f"Details of failure: ")

        for ex_ in result_["failure"]:
            print(f"Exception: {ex_}")
