from model.mail_model import MailModel


class MailTemplateModel(MailModel):
    def __init__(self, mail_subject: str, mail_content: str):
        super().__init__(mail_subject, mail_content)