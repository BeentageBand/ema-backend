from django.db import models


# Create your models here.

# Regular model

class User(object):
    def __init__(self, email):
        self.email = email

# DataBase Model
class Event(models.Model):
    name = models.CharField(max_length=100)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class SignUp(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField(max_length=128)
    signup_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'email'], name='signup')
        ]

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.event.name, self.email)