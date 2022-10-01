from rest_framework import serializers
from .models import ProviderModel, ProviderService
from users.serializers import UserModelSerializer
from services.serializers.serializer_models import ProductSerializer
from locations.serializers import LocationCountySerializer


class ProviderSerializer(serializers.ModelSerializer):
    User = UserModelSerializer(read_only=True, source="UserProviderID")

    class Meta:
        model = ProviderModel
        fields = [
            "id", "User"
        ]


class ProviderServiceSerializer(serializers.ModelSerializer):
    Provider = ProviderSerializer(read_only=True, source="providerID")
    Service = ProductSerializer(read_only=True, source="providerProductID")
    Location = LocationCountySerializer(source="providerLocation", read_only=True)

    class Meta:
        model = ProviderService
        fields = [
            "id", "Provider", "ProviderServiceName", "Service", "AgeBracket",
            "Location", "workingDays"
        ]
