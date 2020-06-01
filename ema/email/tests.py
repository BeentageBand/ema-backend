from .confirmationemail import EventConfirmationEmail
from .emailhandler import EmailHandler
from ema.models import Event

from django.test import TestCase


class EmailHandlerTest(TestCase):

    def setUp(self):
        self.config = {
            'host': 'localhost',
            'port': 1025,
            'ssl': False,
            'username': '',
            'password': ''
        }

        self.email_handler = EmailHandler(config=self.config)
        self.event = Event(name='Event', begin_date='2020-05-29 06:00+00:00', end_date='2020-05-29 18:00+00:00')

    def test_email_confirmation(self):
        confirmation = EventConfirmationEmail('example@example.com', 'example@example.com', self.event)

        try:
            self.email_handler.send_email(confirmation.get_message())
        except RuntimeError:
            self.fail('No Error should occur')

