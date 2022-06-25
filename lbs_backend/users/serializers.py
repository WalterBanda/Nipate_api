from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    CustomUser, Gender
)

UserModel = get_user_model()

class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = "__all__"

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id", "MobileNumber", "IDNumber", "FirstName"
        ]
    
    def validate_MobileNumber(self, MobileNumber):
        if not MobileNumber:
            raise serializers.ValidationError("Please set MobileNumber")
        return MobileNumber
    def validate_IDNumber(self, IDNumber):
        if IDNumber is None:
            raise serializers.ValidationError("Please set IDNumber")
        return IDNumber

class userRegistrationSerializer(serializers.Serializer):
    MobileNumber = serializers.CharField(max_length=10)
    IDNumber = serializers.IntegerField()
    FirstName = serializers.CharField(max_length=50)
    password= serializers.CharField(min_length=8)