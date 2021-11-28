from django.contrib import admin
from .models import Profile, PhysicalActivity


@admin.register(PhysicalActivity)
class PhysicalActivityAdminModel(admin.ModelAdmin):
	pass


@admin.register(Profile)
class ProfileAdminModel(admin.ModelAdmin):
	pass

