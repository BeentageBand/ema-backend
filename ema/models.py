from django.db import models

# Create your models here.

class UserRequest(object):
    """
    Object use in UserRequestSerializer to handle request.data
    """

    def __init__(self, username=None, email=None, signups=[]):
        self.username = username
        self.email = email
        self.signups = signups


# DataBase Model
class Event(models.Model):
    """
    Event DB Model
    """
    name = models.CharField(max_length=100,
                            help_text="Event\'s name")
    begin_date = models.DateTimeField(help_text='Event begin date, it should be before end date')
    end_date = models.DateTimeField(help_text='Event end date, it should be after begin date')
    location = models.CharField(max_length=255, null=True, blank=True,
                                help_text="Event\'s location. It's as description only")

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class SignUp(models.Model):
    """
    SignUp DB Model
    event and email have to be unique.
    """
    event = models.ForeignKey(Event, related_name='signups', on_delete=models.CASCADE,
                              help_text='Event entry, it should be a unique pair with User')
    email = models.EmailField(max_length=64, help_text='User entry, it should be a unique pair with Event.')
    signup_date = models.DateTimeField(auto_now=True, help_text='Date when signup was created')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'email'], name='signup')
        ]

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.event.name, self.email)
