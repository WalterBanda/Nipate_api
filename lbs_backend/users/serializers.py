from rest_framework import serializers
from django.contrib.auth import get_user_model
from locations.serializers import CountyModelSerializers
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
            "id", "mobileNumber", "idNumber", "firstName", "surName"
        ]

    @staticmethod
    def validate_MobileNumber(mobileNumber):
        if not mobileNumber:
            raise serializers.ValidationError("Please set MobileNumber")
        return mobileNumber

    @staticmethod
    def validate_IDNumber(idNumber):
        if idNumber is None:
            raise serializers.ValidationError("Please set IDNumber")
        return idNumber


class userDetailsValidationSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField(max_length=12,
                                         min_length=12, error_messages={'blank': 'invalid mobile number',
                                                                        'length': 'invalid mobile number'})
    idNumber = serializers.IntegerField()
    firstName = serializers.CharField(max_length=50)
    surName = serializers.CharField(max_length=50)


class userPutDetailSerializer(serializers.Serializer):
    userID = serializers.IntegerField()
    locationID = serializers.IntegerField()
    genderID = serializers.IntegerField()
    password = serializers.CharField(min_length=8)


class tokenSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class CreateAuthToken(serializers.Serializer):
    mobileNumber = serializers.CharField(max_length=12, min_length=10)
    password = serializers.CharField(min_length=4)


class LoginResponseSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    auth_token = serializers.CharField()


# All User Details serializer

class AllDetailSerializer(serializers.ModelSerializer):
    location = CountyModelSerializers(read_only=True, source="locationID", many=False)
    gender = GenderSerializer(read_only=True, source="genderID", many=False)

    class Meta:
        model = CustomUser
        fields = [
            "id", "mobileNumber", "idNumber", "firstName", "surName",
            "location", "gender"
        ]
