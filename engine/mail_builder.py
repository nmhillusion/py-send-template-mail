__all__ = ["MailTemplateBuilder", "build_template_with_variables"]

from model import MailTemplateModel


class MailTemplateBuilder:
    def __init__(self, template_model: MailTemplateModel):
        self.template_model = template_model

    def build(self, send_item: dict[str, str]):
        # for key_ in send_item.keys():
        #     value_ = send_item[key_] if send_item[key_] is not None else ""
        #     mail_content_ = mail_content_.replace(f"#{{{key_}}}", value_)
        #     mail_subject_ = mail_subject_.replace(f"#{{{key_}}}", value_)

        clone_mail_model: MailTemplateModel = self.template_model.clone()
        clone_mail_model.mail_subject = build_template_with_variables(self.template_model.mail_subject, send_item)
        clone_mail_model.mail_content = build_template_with_variables(self.template_model.mail_content, send_item)

        return clone_mail_model


def build_template_with_variables(template_content: str, send_item: dict[str, str]):
    out_content_ = template_content
    for key_ in send_item.keys():
        value_ = send_item[key_] if send_item[key_] is not None else ""
        out_content_ = out_content_.replace(f"#{{{key_}}}", value_)

    return out_content_
