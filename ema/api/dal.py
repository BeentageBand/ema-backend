from django.db.utils import IntegrityError
from rest_framework.exceptions import NotFound, ParseError
from ema.models import Event, SignUp, User


# Model DAL
class DAL(object):
    def get_event(self, event_id):
        try:
            model = Event.objects.get(pk=event_id)
            return model
        except Event.DoesNotExist:
            raise NotFound('Event with id {} is not found'.format(event_id))

    def get_signup(self, event_id, signup_id):
        event = self.get_event(event_id)
        try:
            signup = event.signups.get(pk=signup_id)
            return signup
        except SignUp.DoesNotExist:
            raise NotFound('Email id {} is not signed up to Event {}'.format(signup_id, event))

    def set_signup(self, event, user):
        try:
            model = SignUp(event=event, email=user.email)
            model.save()
        except IntegrityError:
            raise ParseError('Email {} is already signed up to Event with id {}')
        return model
