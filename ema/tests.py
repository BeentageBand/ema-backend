from django.db.utils import IntegrityError
from django.test import TestCase
from .models import Event, SignUp
from datetime import datetime

EVENT_VALID_ID = 1
EVENT_INVALID_ID = 100
EVENT_NAME = 'EVENT'
EVENT_BEGIN_DATE = '2020-05-29 06:00+00:00'
EVENT_END_DATE = '2020-05-29 18:00+00:00'
SIGNUP_VALID_ID = 1
SIGNUP_INVALID_ID = 100
SIGNUP_EMAIL = 'dummy@dummy.com'


# Create your tests here.

class EventModelTest(TestCase):
    def setUp(self):
        Event.objects.create(name=EVENT_NAME, begin_date=EVENT_BEGIN_DATE, end_date=EVENT_END_DATE)

    def test_event_doesnt_exist(self):
        try:
            Event.objects.get(pk=EVENT_INVALID_ID)
            self.fail(f'Event with id {EVENT_INVALID_ID} exists')
        except Event.DoesNotExist:
            pass

    def test_event_does_exist(self):
        try:
            event = Event.objects.get(pk=EVENT_VALID_ID)
            self.assertEqual(event.name, EVENT_NAME, 'Event name does not match')
            self.assertEqual(event.begin_date, datetime.fromisoformat(EVENT_BEGIN_DATE),
                             'Event begin_date does not match')
            self.assertEqual(event.end_date, datetime.fromisoformat(EVENT_END_DATE),
                             'Event end_date does not match')
        except Event.DoesNotExist:
            self.fail(f'Event with id {EVENT_VALID_ID} exists')


class SignUpModelTest(TestCase):

    def setUp(self):
        self.event = Event(name=EVENT_NAME, begin_date=EVENT_BEGIN_DATE, end_date=EVENT_END_DATE)
        self.event.save()
        self.event.signups.create(event=self.event, email=SIGNUP_EMAIL)
        self.event.save()

    def test_signup_doesnt_exist(self):
        try:
            SignUp.objects.get(pk=SIGNUP_INVALID_ID)
            self.fail(f'SignUp with id {SIGNUP_INVALID_ID} exists')
        except SignUp.DoesNotExist:
            pass

    def test_signup_does_exist(self):
        try:
            signup = SignUp.objects.get(pk=SIGNUP_VALID_ID)
            self.assertEqual(signup.email, SIGNUP_EMAIL, 'SignUp emails do not match')
        except SignUp.DoesNotExist:
            self.fail(f'SignUp with id {SIGNUP_VALID_ID} exists')

    def test_signup_duplicate_email_raise_error(self):
        try:
            SignUp.objects.create(event=self.event, email=SIGNUP_EMAIL)
            self.fail('Created duplicated email')
        except IntegrityError:
            pass
