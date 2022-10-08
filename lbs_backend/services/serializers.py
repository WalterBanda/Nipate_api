from rest_framework.serializers import ModelSerializer
from .models import (
    WorkingDays, ServiceCategory, Service, Advertisement
)

from users.serializers import UserModelSerializer
from locations.serializers import CountyModelSerializers


class WorkingDaySerializer(ModelSerializer):
    class Meta:
        model = WorkingDays
        fields = ["days"]


class ServiceCategorySerailizer(ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "Name", "CategoryID"]


class InverseServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "Name"]


class InverseCategorySerializer(ModelSerializer):
    services = InverseServiceSerializer(source="category", many=True, read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ["id", "Name", "services"]


class AdvertisementSerializer(ModelSerializer):
    User = UserModelSerializer(source="UserID", read_only=True, many=False)
    Location = CountyModelSerializers(source="LocationID", read_only=True, many=False)
    Service = InverseServiceSerializer(source="ServiceID", read_only=True, many=False)

    class Meta:
        model = Advertisement
        fields = [
            "id", "ADTitle", "User", "Service", "Location", "AdDescription", "StartDate", "ExpiryDate",
            "NoOfMessages"
        ]
