__all__ = ["TestMailTemplateBuilder"]

from unittest import TestCase

from engine import MailTemplateBuilder
from model import MailTemplateModel, MailModel


class TestMailTemplateBuilder(TestCase):

    def test_build(self):
        builder_ = MailTemplateBuilder(
            MailTemplateModel(
                mail_subject="welcome, #{name}",
                mail_content=r"""
                    Dear #{name},
                    Welcome to the forum.
                    Your bill is $#{cost}.
                """
            )
        )

        mail_model_: MailModel = builder_.build({
            "to_emails": "nguyenminhhieu.geek@gmail.com",
            "cc_emails": None,
            "bcc_emails": None,
            "attachments": None,
            "name": "Melynn",
            "cost": "9000000"
        })

        self.assertEqual("welcome, Melynn", mail_model_.mail_subject, "check subject")
        self.assertEqual(r"""
                    Dear Melynn,
                    Welcome to the forum.
                    Your bill is $9000000.
        """.strip(), mail_model_.mail_content.strip(), "check content")
