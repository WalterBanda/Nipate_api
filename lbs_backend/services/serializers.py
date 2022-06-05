from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    WorkingDays
)

class WorkingDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingDays
        fields = ["days"]
