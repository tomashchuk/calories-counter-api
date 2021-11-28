from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

from model_utils import FieldTracker

from calculator.utils import calculate_dci


class PhysicalActivity(models.Model):
    name = models.CharField(max_length=100)
    coef = models.DecimalField(decimal_places=3, max_digits=5)

    class Meta:
        ordering = ['coef', ]

    def __str__(self):
        return self.name


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
        self.calories_norm = round(calculate_dci(self))
        super(Profile, self).save(*args, **kwargs)


class EatingCategory(models.Model):
    options = (
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
        ('snacks', 'snacks'),
    )
    name = models.CharField(max_length=50, choices=options)

    def __str__(self):
        return self.name


class FoodCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)
    # slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        # unique_together = (('parent', 'slug',))
        verbose_name_plural = 'food_categories'

    # def get_slug_list(self):
    #     try:
    #         ancestors = self.get_ancestors(include_self=True)
    #     except:
    #         ancestors = []
    #     else:
    #         ancestors = [i.slug for i in ancestors]
    #     slugs = []
    #     for i in range(len(ancestors)):
    #         slugs.append('/'.join(ancestors[:i + 1]))
    #     return slugs

    def __str__(self):
        return self.name


class Fooditem(models.Model):
    name = models.CharField(max_length=200)
    category = TreeForeignKey(FoodCategory, on_delete=models.CASCADE)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name


