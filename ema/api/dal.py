from django.db.models import Q
from django.db.utils import IntegrityError
from ema.models import Event, SignUp
from rest_framework.exceptions import NotFound, ParseError
from django.contrib.auth.models import User


# Model DAL
class DAL(object):
    """
    Data Abstraction Layer.
    This class handles Event, SignUp data models
    """

    def list_events(self):
        return Event.objects.all()

    def get_signups_by_email(self, email):
        return SignUp.objects.filter(Q(email=email))

    def get_event(self, event_id, email=None):

        try:
            event = Event.objects.get(pk=event_id)
            if email:
                self.get_signup_by_email_or_raise(event, email)
            return event
        except Event.DoesNotExist:
            raise NotFound('Event with id {} is not found'.format(event_id))

    def get_signup(self, event_id, signup_id):
        event = self.get_event(event_id)
        try:
            signup = event.signups.get(pk=signup_id)
            return signup
        except SignUp.DoesNotExist:
            raise NotFound('SignUp id {} is not signed up to Event {}'.format(signup_id, event))

    def set_signup(self, event, email):
        user = User.objects.filter(Q(email=email))

        if not user:
            raise NotFound('Email {} does not belong to any user'.format(email))
        try:
            model = SignUp(event=event, email=email)
            model.save()
        except IntegrityError:
            raise ParseError('Email {} is already signed up to Event {}'.format(email, event))
        return model

    def delete_signup_by_email(self, event_id, email):
        event = self.get_event(event_id)
        signup = self.get_signup_by_email_or_raise(event, email)
        signup.delete()

    def get_signup_by_email_or_raise(self, event, email):
        signup = event.signups.filter(Q(email=email))

        if not signup:
            raise NotFound('Email id {} is not signed up to Event {}'.format(email, event))
        return signup
