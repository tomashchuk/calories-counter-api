from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Profile, PhysicalActivity, EatingCategory, FoodCategory, FoodItem


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

