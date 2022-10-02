from django.contrib import admin
from .models import CountyModel, CenterLocation


@admin.register(CountyModel)
class CountyModelAdmin(admin.ModelAdmin):
    list_display = [
        "id", "Name"
    ]


@admin.register(CenterLocation)
class CenterLocationAdmin(admin.ModelAdmin):
    list_display = [
        "DisplayName", "State", "Town", "Suburb", "Road"
    ]
