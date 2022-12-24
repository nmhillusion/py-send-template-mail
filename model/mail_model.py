__all__ = ["MailModel"]

import yaml
from yaml import SafeLoader


class MailModel:
    def __init__(self, mail_subject: str, mail_content: str):
        self.mail_content = mail_content
        self.mail_subject = mail_subject

    @classmethod
    def from_file(cls, file_name_: str, encoding_: str = 'utf8'):
        with open(file_name_, encoding='utf-8') as f_:
            content = yaml.load(f_, Loader=SafeLoader)
            mail_content_template_path_ = content["mail_content"]["template-path"]
            mail_content_encoding_ = content["mail_content"]["encoding"]
            with open(mail_content_template_path_,
                      encoding=mail_content_encoding_ if not None else "utf-8"
                      ) as mail_content_f_:
                return MailModel(mail_subject=content["mail_subject"], mail_content=mail_content_f_.read())
