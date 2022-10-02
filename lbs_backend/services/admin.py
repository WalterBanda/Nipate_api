from django.contrib import admin
from .models import (
    WorkingDays, ServiceCategory, Service
)

admin.site.register(ServiceCategory)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ["id", "days"]

