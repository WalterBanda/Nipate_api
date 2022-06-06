from rest_framework.serializers import ModelSerializer

from .models import TownsModel, CountyModel


class TownsModelSerializer(ModelSerializer):
    
    class Meta:
        model = TownsModel
        fields = ["id", "Name"]