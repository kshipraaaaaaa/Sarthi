from django.contrib import admin
from .models import LocationSharing, FamilyConnection


@admin.register(LocationSharing)
class LocationSharingAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'is_enabled',
        'latitude',
        'longitude',
        'updated_at'
    )


@admin.register(FamilyConnection)
class FamilyConnectionAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'parent',
        'status',
        'created_at'
    )
