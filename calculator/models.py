from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from model_utils import FieldTracker

from calculator.utils import calculate_dci


class PhysicalActivity(models.Model):
    name = models.CharField(max_length=100)
    coef = models.DecimalField(decimal_places=3, max_digits=5)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_activity = models.ForeignKey(PhysicalActivity, on_delete=models.PROTECT)
    sex = models.CharField(max_length=10, choices=(("Male", "male"), ("Female", "female")))
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    birth_date = models.DateField()

    calories_norm = models.PositiveIntegerField()

    tracker = FieldTracker()

    @property
    def age(self):
        return datetime.now().date() - self.birth_date

    def save(self, *args, **kwargs):
        self.calories_norm = round(calculate_dci())
        super(Profile, self).save(*args, **kwargs)


