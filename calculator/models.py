from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    birth_date = models.DateField()
