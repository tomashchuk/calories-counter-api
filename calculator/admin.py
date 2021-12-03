from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Profile,
    PhysicalActivity,
    EatingCategory,
    FoodCategory,
    FoodItem,
    FoodEvent,
)


@admin.register(PhysicalActivity)
class PhysicalActivityAdminModel(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdminModel(admin.ModelAdmin):
    pass


@admin.register(EatingCategory)
class EatingCategoryAdminModel(admin.ModelAdmin):
    pass


@admin.register(FoodCategory)
class FoodCategoryAdminModel(MPTTModelAdmin):
    pass


@admin.register(FoodItem)
class FoodItemAdminModel(admin.ModelAdmin):
    pass


@admin.register(FoodEvent)
class FoodEventAdminModel(admin.ModelAdmin):
    pass
