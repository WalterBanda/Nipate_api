from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.serializers import ProductSerializer
from locations.serializers import LocationSerializer
from .models import (
    Provider, User, Gender, WorkingDays
)

UserModel = get_user_model()


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = "__all__"


class WorkingDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingDays
        fields = ["days"]

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id", "MobileNumber", "IDNumber", "FirstName"
        ]


class ProviderSerializer(serializers.ModelSerializer):

    User = UserModelSerializer(read_only=True, source="UserID")
    Product = ProductSerializer(read_only=True, source="ProductID")
    Location = LocationSerializer(read_only=True, source="LocationID")
    Gender = GenderSerializer(read_only=True, source="GenderID")
    WorkingDays = WorkingDaySerializer(read_only=True, many=True, source="WorkingDaysID")

    class Meta:
        model = Provider
        geo_field = "Coordinates"
        fields = [
            'id', 'User', 'Product', 'Location', 'Gender',
            'Coordinates', 'AgeBracket', 'WorkingDays'
        ]

class MiniProviderSerializer(serializers.ModelSerializer):
    
    User = UserModelSerializer(read_only=True, source="UserID")
    class Meta:
        model = Provider
        fields = [
            'id', 'User'
        ]