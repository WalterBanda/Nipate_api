from abc import ABC

from rest_framework import serializers
from .models import ProviderModel, ProviderService, ServiceResponse, ServiceRequest
from users.serializers import UserModelSerializer
from locations.serializers import CenterLocationSerializer, CountyModelSerializers


class ProviderSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True, source="userID", many=False)
    county = CountyModelSerializers(source="countyID", read_only=True, many=False)

    class Meta:
        model = ProviderModel
        fields = [
            "id", "user", "county"
        ]


class CreateProviderSerializer(serializers.Serializer):
    countyID = serializers.IntegerField()


class ProviderServiceSerializer(serializers.ModelSerializer):
    from services.serializers import ServiceSerializer
    provider = ProviderSerializer(read_only=True, source="providerID")
    service = ServiceSerializer(read_only=True, source="productID")
    location = CenterLocationSerializer(source="centerLocationID", read_only=True)

    class Meta:
        model = ProviderService
        fields = [
            "id", "provider", "serviceTitle", "service", "serviceDescription", "longitude", "lattitude",
            "location", "workingDays", "ageBracket",
        ]


class CreatePostProviderServiceSerializer(serializers.Serializer):
    serviceTitle = serializers.CharField()
    productID = serializers.IntegerField()
    serviceDescription = serializers.CharField(allow_null=True, allow_blank=True)
    longitude = serializers.CharField(max_length=50)
    lattitude = serializers.CharField(max_length=50)
    centerLocationID = serializers.IntegerField()


class SearchCenterLocationSerializer(serializers.Serializer):
    longitude = serializers.CharField(max_length=50)
    lattitude = serializers.CharField(max_length=50)


class UserStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserModelSerializer(many=False)
    location = CountyModelSerializers(many=False)
    provider = serializers.BooleanField()


class ServiceRequestSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True, source="userID", many=False)
    service = ProviderServiceSerializer(source="providerServiceID", many=False)
    centerLocation = CenterLocationSerializer(source="centerLocationID", many=False)

    class Meta:
        model = ServiceRequest
        fields = [
            "id", "user", "service", "centerLocation", "timeStamp", "requestText", "latitude", "longitude"
        ]


class ServiceResponseSerializer(serializers.ModelSerializer):
    request = ServiceRequestSerializer(source="serviceRequestID", many=False)

    class Meta:
        model = ServiceResponse
        fields = [
            "id", "request", "responseText", "timeStamp"
        ]


class CreateServiceRequestSerializer(serializers.Serializer):
    providerServiceID = serializers.IntegerField()
    requestText = serializers.CharField(allow_blank=True, allow_null=True)
    centerLocationID = serializers.IntegerField(allow_null=True)
    latitude = serializers.CharField(allow_blank=True, allow_null=True)
    longitude = serializers.CharField(allow_blank=True, allow_null=True)


class CreateServiceResponseSerializer(serializers.Serializer):
    serviceRequestID = serializers.IntegerField()
    responseText = serializers.CharField(allow_blank=True, allow_null=True)


class SearchServiceSerializer(serializers.Serializer):
    searchdata = serializers.CharField()
    serviceCategory = serializers.CharField(allow_blank=True)
    region = serializers.CharField(allow_blank=True)
