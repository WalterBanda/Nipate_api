from django.contrib import admin
from .models import ProviderModel, ProviderService, ServiceRequest, ServiceResponse


@admin.register(ProviderModel)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'userID', 'countyID']


@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'serviceTitle', 'providerID', 'productID', 'centerLocationID']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "userID", "providerServiceID", "centerLocationID", "timeStamp"]


@admin.register(ServiceResponse)
class ServiceResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "serviceRequestID", "responseText", "timeStamp"]
