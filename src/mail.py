from typing import List, Union
from flask_mail import Message, Mail as FlaskMail
from flask import current_app as app


class Mail:
    def __init__(self, flask_mail: FlaskMail):
        self._flask_mail = flask_mail

    def send(self, subject: str, html: str, recipients: List[Union[str, None]]):
        unsubscribe_mail = app.config["MAIL_UNSUBSCRIBE_USERNAME"]
        unsubscribe_link = f"<mailto: {unsubscribe_mail}?subject=unsubscribe>"
        msg = Message(
            subject=subject,
            sender=app.config["MAIL_USERNAME"],
            reply_to=app.config["MAIL_USERNAME"],
            recipients=recipients,
            extra_headers={"list-unsubscribe": unsubscribe_link, "Precedence": "Bulk"},
            charset="utf-8",
            html=html,
        )

        if app.config.get("DEBUG"):
            print(
                {"subject": subject, "html": html, "recipients": recipients,}
            )
        else:
            self._flask_mail.send(msg)
