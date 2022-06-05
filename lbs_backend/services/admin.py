from django.contrib import admin
from .models import (
    WorkingDays, ProductCategory, Product, ServiceProvider
)

class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = [
        "id", "days"
    ]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'ProductID', 'LocationID', 'GenderID', 'TimeStamp']

admin.site.register(WorkingDays, WorkingDaysAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)