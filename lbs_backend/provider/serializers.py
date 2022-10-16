from rest_framework import serializers
from .models import ProviderModel, ProviderService
from users.serializers import UserModelSerializer
from services.serializers import ServiceSerializer
from locations.serializers import CenterLocationSerializer, CountyModelSerializers


class ProviderSerializer(serializers.ModelSerializer):
    User = UserModelSerializer(read_only=True, source="UserID", many=False)
    County = CountyModelSerializers(source="CountyID", read_only=True, many=False)

    class Meta:
        model = ProviderModel
        fields = [
            "id", "User", "County"
        ]


class CreateProviderSerializer(serializers.Serializer):
    CountyID = serializers.IntegerField()


class ProviderServiceSerializer(serializers.ModelSerializer):
    Provider = ProviderSerializer(read_only=True, source="ProviderID")
    Service = ServiceSerializer(read_only=True, source="ProductID")
    Location = CenterLocationSerializer(source="CenterLocationID", read_only=True)

    class Meta:
        model = ProviderService
        fields = [
            "id", "Provider", "ServiceTitle", "Service", "ServiceDescription", "Longitude", "Lattitude",
            "Location", "workingDays", "AgeBracket",
        ]


class CreatePostProviderServiceSerializer(serializers.Serializer):
    ServiceTitle = serializers.CharField()
    ProductID = serializers.IntegerField()
    ServiceDescription = serializers.CharField(allow_null=True, allow_blank=True)
    Longitude = serializers.CharField(max_length=50)
    Lattitude = serializers.CharField(max_length=50)
    CenterLocationID = serializers.IntegerField()


class SearchCenterLocationSerializer(serializers.Serializer):
    Longitude = serializers.CharField(max_length=50)
    Lattitude = serializers.CharField(max_length=50)


class UserStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    User = UserModelSerializer(many=False)
    Location = CountyModelSerializers(many=False)
    Provider = serializers.BooleanField()
