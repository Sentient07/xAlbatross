from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Journey(models.Model):
    passenger = models.ForeignKey(User)
    source_location = models.CharField(max_length=20)
    destination_location = models.CharField(max_length=20)
    booking_date = models.DateTimeField(auto_now=True)
    number_of_tickets = models.IntegerField()
    transportation_mode = models.CharField()
    journey_date = models.DateTimeField()


class ModeofTransport(models.Model):
    modes = models.CharField()