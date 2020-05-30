from restserver.settings import SMTP_CONFIG
from smtplib import SMTP, SMTP_SSL, SMTPNotSupportedError


class EmailHandler:
    def __init__(self):
        self.config = SMTP_CONFIG
        self.provide_smtp = SMTP_SSL if SMTP_CONFIG['ssl'] else SMTP

    def auth(self, client):
        try:
            client.login(self.config['username'], self.config['password'])
        except SMTPNotSupportedError:
            pass  # TODO : handle login error

    def send_email(self, email_message):
        client = self.provide_smtp(self.config['host'], self.config['port'])
        self.auth(client)
        client.send_message(email_message)
        client.close()
