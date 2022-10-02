from rest_framework.serializers import ModelSerializer

from .models import CountyModel, CenterLocation


class CountyModelSerializers(ModelSerializer):
    class Meta:
        model = CountyModel
        fields = ["id", "Name"]


class CenterLocationSerializer(ModelSerializer):
    class Meta:
        model = CenterLocation
        fields = "__all__"
