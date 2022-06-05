from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    CustomUser, Gender, WorkingDays
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