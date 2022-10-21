from django.contrib import admin
from .models import ProviderModel, ProviderService, ServiceRequest, ServiceResponse


@admin.register(ProviderModel)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['UserID', 'CountyID']


@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = ['ServiceTitle', 'ProviderID', 'ProductID', 'CenterLocationID']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "UserID", "ProviderServiceID", "CenterLocationID", "TimeStamp"]


@admin.register(ServiceResponse)
class ServiceResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "ServiceRequestID", "ResponseText", "TimeStamp"]
