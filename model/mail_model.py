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
            return MailModel(mail_subject=content["mail_subject"], mail_content=content["mail_content"])