from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

from model_utils import FieldTracker

from calculator.utils import (
    calculate_dci,
    FATS_PERCENTAGE_FROM_DCI,
    PROTEIN_PERCENTAGE_FROM_DCI,
    calculate_water_norm,
)


class PhysicalActivity(models.Model):
    name = models.CharField(max_length=100)
    coef = models.DecimalField(decimal_places=3, max_digits=5)

    class Meta:
        ordering = [
            "coef",
        ]

    def __str__(self):
        return self.name


class Profile(models.Model):
    """User profile representation. Recalculates needed fats ... on each saving"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_activity = models.ForeignKey(PhysicalActivity, on_delete=models.PROTECT)
    sex = models.CharField(
        max_length=10, choices=(("male", "male"), ("female", "female"))
    )
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    birth_date = models.DateField()

    calories_norm = models.PositiveIntegerField(null=True, blank=True)
    fats_norm = models.PositiveIntegerField(null=True, blank=True)
    protein_norm = models.PositiveIntegerField(null=True, blank=True)
    carbohydrate_norm = models.PositiveIntegerField(null=True, blank=True)
    water_norm = models.PositiveIntegerField(null=True, blank=True)

    tracker = FieldTracker()

    @property
    def age(self):
        return (datetime.now().date() - self.birth_date).days // 365

    def save(self, *args, **kwargs):
        self.calories_norm = round(calculate_dci(self))
        self.fats_norm = round(self.calories_norm * FATS_PERCENTAGE_FROM_DCI)
        self.protein_norm = round(self.calories_norm * PROTEIN_PERCENTAGE_FROM_DCI)
        self.carbohydrate_norm = round((self.calories_norm / 2) / 4)
        self.water_norm = round(calculate_water_norm(self))
        super(Profile, self).save(*args, **kwargs)


class EatingCategory(models.Model):
    """Eating category representation"""
    options = (
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Snacks", "Snacks"),
    )
    name = models.CharField(max_length=50, choices=options, unique=True)
    # image = models.ImageField(upload_to="eating-category")
    order = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        ordering = [
            "order",
        ]

    def __str__(self):
        return self.name


class FoodCategory(MPTTModel):
    """Tree representation of general food category"""
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.PROTECT
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "food_categories"

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """Represents food. Includes common info about food item"""
    name = models.CharField(max_length=200)
    category = TreeForeignKey(FoodCategory, on_delete=models.CASCADE)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.name


class WaterEvent(models.Model):
    """
    Water Event representation
    ordering: -created
    """
    created = models.DateTimeField(auto_created=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        ordering = [
            "-created",
        ]


class FoodEvent(models.Model):
    """
    Water Event representation
    """
    eating_category = models.ForeignKey(EatingCategory, on_delete=models.PROTECT)
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = [
            "-created",
        ]
