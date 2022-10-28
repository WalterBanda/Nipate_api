from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
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
        fields = ["id", "name", "categoryID"]


class InverseServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class InverseCategorySerializer(ModelSerializer):
    services = InverseServiceSerializer(source="category", many=True, read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "services"]


class AdvertisementSerializer(ModelSerializer):
    from provider.serializers import ProviderSerializer
    provider = ProviderSerializer(source="providerID", read_only=True, many=False)
    location = CountyModelSerializers(source="locationID", read_only=True, many=False)
    service = InverseServiceSerializer(source="serviceID", read_only=True, many=True)

    class Meta:
        model = Advertisement
        fields = [
            "id", "title", "provider", "service", "location", "description", "startDate", "expiryDate",
            "noOfMessages"
        ]


class CreateAdvertSerializer(Serializer):
    title = serializers.CharField()
    providerID = serializers.IntegerField()
    serviceID = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    locationID = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True)
    startDate = serializers.DateField(allow_null=True)
    expiryDate = serializers.DateField()
