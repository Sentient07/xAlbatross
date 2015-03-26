from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):

    user = models.ForeignKey(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    mobile_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'
