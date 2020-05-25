from django.db import models


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)
