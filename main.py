import json

import pandas as pd
from pandas import DataFrame

from mail_engine import MailTemplateBuilder, MailTemplateModel, MailModel, send_mail


def parse_data_file_to_send_items():
    data_: DataFrame = pd.read_excel("./data.xlsx", sheet_name=0, header=0, converters={"agent_code": str})

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


def read_mail_template():
    return MailTemplateModel.from_file("./mail_template.yml")


def run():
    mail_template_: MailTemplateModel = read_mail_template()
    mail_builder_ = MailTemplateBuilder(mail_template_)

    send_items_ = parse_data_file_to_send_items()

    result_ = {"success": 0, "failure": []}
    for si_ in send_items_:
        try:
            to_emails_ = si_["to_emails"]
            cc_emails_ = si_["cc_emails"]
            bcc_emails_ = si_["bcc_emails"]
            attachments_ = si_["attachments"]

            if to_emails_ is None:
                raise Exception("Cannot execute on None to_emails")

            mail_model_: MailModel = mail_builder_.build(si_)
            send_mail(mail_model=mail_model_, to_emails=to_emails_, cc_emails=cc_emails_, bcc_emails=bcc_emails_, attachments=attachments_)

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
