__all__ = ["MailModel"]

import yaml
from yaml import SafeLoader


class MailModel:
    def __init__(self, mail_subject: str, is_template: bool, mail_template_path: str, mail_content: str):
        self.mail_subject = mail_subject
        self.is_template = is_template
        self.mail_template_path = mail_template_path
        self.mail_content = mail_content

    @classmethod
    def from_file(cls, file_name_: str):
        with open(file_name_, encoding='utf-8') as f_:
            content = yaml.load(f_, Loader=SafeLoader)
            is_template_: bool = content["is_template"]
            mail_content_template_path_ = content["mail_content"]["template-path"]
            mail_content_encoding_ = content["mail_content"]["encoding"]
            mail_template_content_ = ""

            if not is_template_:
                with open(mail_content_template_path_,
                          encoding=mail_content_encoding_ if not None else "utf-8"
                          ) as mail_content_f_:
                    mail_template_content_ = mail_content_f_.read()

            return MailModel(mail_subject=content["mail_subject"],
                             is_template=is_template_,
                             mail_template_path=mail_content_template_path_,
                             mail_content=mail_template_content_)

    def clone(self):
        return MailModel(
            self.mail_subject
            , self.is_template
            , self.mail_template_path
            , self.mail_content
        )
