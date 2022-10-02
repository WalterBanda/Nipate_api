from django.contrib import admin
from .models import (
    WorkingDays, ServiceCategory, Service
)

admin.site.register(ServiceCategory)


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ["id", "days"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']
