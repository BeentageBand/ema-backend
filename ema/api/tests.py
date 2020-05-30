from .dal import DAL
from django.test import TestCase
from datetime import datetime
from ema.models import Event, SignUp, User
from rest_framework.exceptions import NotFound, ParseError


# Create your tests here.

class DALTest(TestCase):
    EVENT_VALID_ID = 1
    EVENT_INVALID_ID = 100
    EVENT_NAME = 'EVENT'
    EVENT_BEGIN_DATE = '2020-05-29 06:00+00:00'
    EVENT_END_DATE = '2020-05-29 18:00+00:00'
    SIGNUP_VALID_ID = 1
    SIGNUP_INVALID_ID = 100
    SIGNUP_EMAIL = 'dummy@dummy.com'
    SIGNUP_NEW_EMAIL = '2' + SIGNUP_EMAIL

    def setUp(self):
        self.dal = DAL()
        self.event = Event(name=self.EVENT_NAME, begin_date=self.EVENT_BEGIN_DATE, end_date=self.EVENT_END_DATE)
        self.event.save()
        SignUp.objects.create(event=self.event, email=self.SIGNUP_EMAIL)

    def test_when_event_does_not_exist_raise_not_found(self):
        try:
            self.dal.get_event(event_id=self.EVENT_INVALID_ID)
            self.fail('Event should not exist')
        except NotFound:
            pass

    def test_when_event_does_exist_return_event(self):
        event = self.dal.get_event(event_id=self.EVENT_VALID_ID)
        self._validate_event(event)

    def test_when_signup_does_not_exist_raise(self):
        try:
            self.dal.get_signup(event_id=self.EVENT_VALID_ID, signup_id=self.SIGNUP_INVALID_ID)
            self.fail('SignUp should not exist')
        except NotFound:
            pass

    def test_when_signup_does_exist_return_signup(self):
        signup = self.dal.get_signup(event_id=self.EVENT_VALID_ID, signup_id=self.SIGNUP_VALID_ID)
        self._validate_signup(signup)

    def test_when_signup_duplicated_email_raise_parse_error(self):
        user = User(email=self.SIGNUP_EMAIL)
        try:
            self.dal.set_signup(self.event, user)
            self.fail('SignUp should not succeed')
        except ParseError:
            pass

    def test_when_signup_new_email(self):
        user = User(email=self.SIGNUP_NEW_EMAIL)
        try:
            signup = self.dal.set_signup(self.event, user)
        except ParseError:
            self.fail('SignUp should succeed')
        self.assertEqual(signup.email, self.SIGNUP_NEW_EMAIL, 'Emails do not match')
        self.assertEqual(self.event, signup.event, 'Events do not match')

    def _validate_event(self, event):
        self.assertEqual(event.name, self.EVENT_NAME, 'Event names dont match')
        self.assertEqual(event.begin_date, datetime.fromisoformat(self.EVENT_BEGIN_DATE),
                         'Event begin dates dont match')
        self.assertEqual(event.end_date, datetime.fromisoformat(self.EVENT_END_DATE), 'Event end dates dont match')

    def _validate_signup(self, signup):
        self.assertEqual(signup.email, self.SIGNUP_EMAIL, 'Signup emails dont match')
