__all__ = ["MailSender"]

from os.path import exists

import win32com.client as win32client

from engine.mail_builder import build_template_with_variables
from gui.component import logging_emitter
from model import MailModel


class MailSender:
    def __init__(self, mail_model: MailModel, send_item: dict[str, str | None]):
        self.mail_model = mail_model
        self.send_item = send_item

    def preview_mail(self):
        return self.exec_mailing(only_preview=True)

    def send_mail(self):
        return self.exec_mailing(only_preview=False)

    def exec_mailing(self, only_preview: bool):
        si_ = self.send_item

        for column_name_ in ["to_emails", "cc_emails", "bcc_emails", "attachments"]:
            if column_name_ not in si_.keys():
                raise IOError(f"excel file is missing required column: {column_name_}")

        to_emails_ = si_["to_emails"]
        cc_emails_ = si_["cc_emails"]
        bcc_emails_ = si_["bcc_emails"]
        attachments_ = si_["attachments"]
        reminder_date_ = si_["reminder_date"]

        if to_emails_ is None:
            raise ValueError("Cannot execute on None to_emails")

        self.__do_send_mail__(
            to_emails=to_emails_,
            cc_emails=cc_emails_,
            bcc_emails=bcc_emails_,
            attachments=attachments_,
            reminder_date=reminder_date_,
            only_preview=only_preview)

    def __do_send_mail__(self, to_emails: str, cc_emails: str, bcc_emails: str, attachments: str | None, reminder_date: str | None, only_preview: bool = True):
        action_name_ = "preview" if only_preview else "send"

        logging_emitter.info(f"will {action_name_} mail to... {to_emails}")
        outlook = win32client.Dispatch("outlook.application")

        if self.mail_model.is_template:
            mail = outlook.CreateItemFromTemplate(self.mail_model.mail_template_path)
        else:
            mail = outlook.CreateItem(0)

        mail.Subject = build_template_with_variables(mail.Subject, self.send_item) \
            if self.mail_model.is_template and mail.Subject is not None \
            else self.mail_model.mail_subject

        mail.To = to_emails

        if cc_emails is not None:
            mail.CC = cc_emails
        if bcc_emails is not None:
            mail.BCC = bcc_emails

        if self.mail_model.is_template:
            mail.HTMLBody = build_template_with_variables(mail.HTMLBody, self.send_item)
        else:
            mail.HTMLBody = self.mail_model.mail_content

        if attachments is not None and 0 < len(attachments.strip()):
            attachments_ = attachments.split(",")
            for att_ in attachments_:
                if att_ is not None:
                    logging_emitter.info(f"attachment: {att_}")

                    att_ = att_.strip()
                    if not exists(att_):
                        raise ValueError(f"Attachment file does not existed of to_mails: {to_emails} - path: {att_}")

                    mail.Attachments.Add(att_.strip())

        logging_emitter.info(f" started {action_name_}ing: {mail}")

        if 0 < len(str(reminder_date)):
            # Set follow-up flag for recipient
            mail.FlagRequest = "Follow up"

            # Set reminder for sender
            mail.ReminderSet = True
            mail.ReminderTime = reminder_date
            mail.FlagDueBy = reminder_date

        if only_preview:
            logging_emitter.info("Previewing...")
            mail.Display(True)
        else:
            logging_emitter.info("Sending...")
            mail.Send()

        logging_emitter.info(f"completed {action_name_}ing mail to... {to_emails}")
