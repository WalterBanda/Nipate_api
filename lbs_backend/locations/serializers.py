from rest_framework.serializers import ModelSerializer

from .models import TownsModel, CountyModel


class TownsModelSerializer(ModelSerializer):
    class Meta:
        model = TownsModel
        fields = ["id", "Name"]


class CountyModelSerializers(ModelSerializer):
    # Towns = TownsModelSerializer(read_only=True, source="counties", many=True)
    class Meta:
        model = CountyModel
        fields = ["id", "Name"]


class LocationSerializer(ModelSerializer):
    Towns = TownsModelSerializer(read_only=True, source="counties", many=True)

    class Meta:
        model = CountyModel
        fields = ["id", "Name", "Towns"]


class LocationCountySerializer(ModelSerializer):
    County = CountyModelSerializers(read_only=True, source="counties")

    class Meta:
        model = TownsModel
        fields = [
            "id", "Name", "County"
        ]
