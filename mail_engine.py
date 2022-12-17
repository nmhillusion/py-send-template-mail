import win32com.client as win32
import yaml
from yaml import SafeLoader


class MailModel:
    def __init__(self, mail_subject: str, mail_content: str):
        self.mail_content = mail_content
        self.mail_subject = mail_subject

    @classmethod
    def from_file(cls, file_name_: str):
        with open(file_name_, encoding='utf8') as f_:
            content = yaml.load(f_, Loader=SafeLoader)
            return MailTemplateModel(mail_subject=content["mail_subject"], mail_content=content["mail_content"])


class MailTemplateModel(MailModel):
    def __init__(self, mail_subject: str, mail_content: str):
        super().__init__(mail_subject, mail_content)


class MailTemplateBuilder:
    def __init__(self, template_model: MailTemplateModel):
        self.template_model = template_model

    def build(self, send_item: dict[str, str]):
        mail_content_ = self.template_model.mail_content
        mail_subject_ = self.template_model.mail_subject

        for key_ in send_item.keys():
            value_ = send_item[key_] if send_item[key_] is not None else ""
            mail_content_ = mail_content_.replace(f"#{{{key_}}}", value_)
            mail_subject_ = mail_subject_.replace(f"#{{{key_}}}", value_)

        return MailTemplateModel(mail_subject=mail_subject_, mail_content=mail_content_)


def send_mail(mail_model: MailModel, to_emails: str, cc_emails: str, bcc_emails: str, attachments: str | None):
    print(f"will do sending mail to... {to_emails}")
    outlook = win32.Dispatch("outlook.application")

    mail = outlook.CreateItem(0)
    mail.Subject = mail_model.mail_subject
    mail.To = to_emails

    if cc_emails is not None:
        mail.CC = cc_emails
    if bcc_emails is not None:
        mail.BCC = bcc_emails

    # attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "currency_img")
    mail.HTMLBody = mail_model.mail_content
    # attachment = mail.Attachments.Add(os.getcwd() + "\\Currencies.png")
    # mail.Attachments.Add(os.getcwd() + "\\Currencies.xlsx")

    if attachments is not None and 0 < len(attachments.strip()):
        attachments_ = attachments.split(",")
        for att_ in attachments_:
            if att_ is not None:
                print(f"attachment: {att_}")
                mail.Attachments.Add(att_.strip())

    print(f" will send: {mail}")
    mail.Send()
    print(f"completed sending mail to... {to_emails}")
