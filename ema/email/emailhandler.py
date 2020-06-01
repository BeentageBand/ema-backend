from restserver.settings import SMTP_CONFIG
from smtplib import SMTP, SMTP_SSL, SMTPNotSupportedError


class EmailHandler:
    def __init__(self, config=SMTP_CONFIG):
        self.host = config['host']
        self.port = config['port']
        self.username = config['username']
        self.password = config['password']
        self.fwd_address = config['emailAddress']
        self.provide_smtp = SMTP_SSL if config['ssl'] else SMTP

    def auth(self, client):
        try:
            client.login(self.username, self.password)
        except SMTPNotSupportedError:
            if isinstance(client, SMTP_SSL) and 'localhost' is not self.host:
                raise ConnectionRefusedError(f'Unable to login {self.host}:{self.port}')

    def send_email(self, email_message):
        email_message['CC'] = self.fwd_address
        print(f'Sending email to {self.host}:{self.port}')
        client = self.provide_smtp(self.host, self.port)
        self.auth(client)
        client.send_message(email_message)
        client.close()
