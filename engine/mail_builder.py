from model.mail_model import MailModel
from model.mail_template_model import MailTemplateModel


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

        return MailModel(mail_subject=mail_subject_, mail_content=mail_content_)
