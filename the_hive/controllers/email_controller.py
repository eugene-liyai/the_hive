"""
File      : email_controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Controls sending email functionality
"""

# ============================================================================
# necessary imports
# ============================================================================
from threading import Thread

from flask_mail import Message

from the_hive import app, mail
from the_hive.util import async


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, html_body, bcc):
    msg = Message(subject=subject, sender=sender, recipients=recipients, bcc=bcc)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
