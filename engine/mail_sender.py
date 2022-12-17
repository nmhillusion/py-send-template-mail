import win32com.client as win32client

from model.mail_model import MailModel


class MailSender:
    def __init__(self, mail_model: MailModel, send_item: dict[str, str | None]):
        self.mail_model = mail_model
        self.send_item = send_item

    def send_mail(self):
        si_ = self.send_item

        for column_name_ in ["to_emails", "cc_emails", "bcc_emails", "attachments"]:
            if column_name_ not in si_.keys():
                raise IOError(f"excel file is missing required column: {column_name_}")

        to_emails_ = si_["to_emails"]
        cc_emails_ = si_["cc_emails"]
        bcc_emails_ = si_["bcc_emails"]
        attachments_ = si_["attachments"]

        if to_emails_ is None:
            raise ValueError("Cannot execute on None to_emails")

        self.__do_send_mail__(to_emails=to_emails_, cc_emails=cc_emails_, bcc_emails=bcc_emails_, attachments=attachments_)

    def __do_send_mail__(self, to_emails: str, cc_emails: str, bcc_emails: str, attachments: str | None):
        print(f"will do sending mail to... {to_emails}")
        outlook = win32client.Dispatch("outlook.application")

        mail = outlook.CreateItem(0)
        mail.Subject = self.mail_model.mail_subject
        mail.To = to_emails

        if cc_emails is not None:
            mail.CC = cc_emails
        if bcc_emails is not None:
            mail.BCC = bcc_emails

        mail.HTMLBody = self.mail_model.mail_content

        if attachments is not None and 0 < len(attachments.strip()):
            attachments_ = attachments.split(",")
            for att_ in attachments_:
                if att_ is not None:
                    print(f"attachment: {att_}")
                    mail.Attachments.Add(att_.strip())

        print(f" will send: {mail}")
        mail.Send()
        print(f"completed sending mail to... {to_emails}")
