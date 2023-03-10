from typing import Callable

from engine import MailTemplateBuilder, MailSender
from gui.component import logging_emitter
from model import MailTemplateModel
from service.data_parser import read_setting, read_mail_template, parse_data_file_to_send_items


######################################################
# MAIN PROGRAM #######################################
######################################################

def preview_send_item(template_file_path_: str, si_: dict[str, str]):
    logging_emitter.info("previewing send item: " + str(si_))
    settings = read_setting()
    mail_template_: MailTemplateModel = read_mail_template(settings["path"]["template"], template_file_path_)
    mail_builder_ = MailTemplateBuilder(mail_template_)

    MailSender(mail_model=mail_builder_.build(si_), send_item=si_).preview_mail()


def send_all_items(template_file_path_: str, data_excel_path_: str, converters_: dict[str, Callable]):
    settings = read_setting()
    mail_template_: MailTemplateModel = read_mail_template(settings["path"]["template"], template_file_path_)
    mail_builder_ = MailTemplateBuilder(mail_template_)

    send_items_ = parse_data_file_to_send_items(data_excel_path_ if not None else settings["path"]["data"], converters_)

    result_ = {"success": 0, "failure": []}
    for si_ in send_items_:
        try:
            MailSender(mail_model=mail_builder_.build(si_), send_item=si_).send_mail()

            result_["success"] += 1
        except Exception as ex:
            logging_emitter.error(f"ERROR: {ex}")
            result_["failure"].append(ex)

    logging_emitter.info(f"==== Running results ===========")
    logging_emitter.info(f"\tSuccess: {result_['success']}")
    logging_emitter.info(f"\tFailure: {len(result_['failure'])}")
    if 0 < len(result_["failure"]):
        logging_emitter.info(f"Details of failure: ")

        for ex_ in result_["failure"]:
            logging_emitter.error(f"Exception: {ex_}")
