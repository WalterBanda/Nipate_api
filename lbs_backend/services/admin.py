from django.contrib import admin
from .models import (
    WorkingDays, ServiceCategory, Service, Advertisement
)

admin.site.register(ServiceCategory)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ["id", "days"]


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "providerID", "locationID", "description", "startDate", "expiryDate",
        "noOfMessages"
    ]
