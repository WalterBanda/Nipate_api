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
    Provider = ProviderSerializer(read_only=True, source="providerID")
    Service = ServiceSerializer(read_only=True, source="providerProductID")
    Location = CenterLocationSerializer(source="providerLocation", read_only=True)

    class Meta:
        model = ProviderService
        fields = [
            "id", "Provider", "ProviderServiceName", "Service", "AgeBracket",
            "Location", "workingDays"
        ]


class CreateProviderServiceSerializer(serializers.Serializer):
    ProviderID = serializers.IntegerField()
    ProviderServiceName = serializers.CharField()
    ProductID = serializers.IntegerField()
    LocationID = serializers.CharField(allow_null=True, allow_blank=True)
    GenderID = serializers.IntegerField(allow_null=True)
    AgeBracket = serializers.CharField(default="All")
    workingDays = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    Longitude = serializers.CharField(allow_null=True, allow_blank=True)
    Lattitude = serializers.CharField(allow_null=True, allow_blank=True)
