__all__ = ["MailTemplateModel"]

from model import MailModel


class MailTemplateModel(MailModel):
    def __init__(self, mail_subject: str, is_template: bool, mail_template_path: str, mail_content: str):
        super().__init__(mail_subject=mail_subject, is_template=is_template, mail_template_path=mail_template_path, mail_content=mail_content)
