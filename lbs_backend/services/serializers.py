from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .models import (
    WorkingDays, ProductCategory, Product, ServiceProvider, ServiceRequest
)
from users.serializers import UserModelSerializer, GenderSerializer
from locations.serializers import TownsModelSerializer
class WorkingDaySerializer(ModelSerializer):
    class Meta:
        model = WorkingDays
        fields = ["days"]

class ProductCategorySerailizer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "Name", "CategoryID"]

class InverseProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "Name"]

class InverseCategorySerializer(ModelSerializer):
    Product = InverseProductSerializer(source="CategoryID")
    class Meta:
        model = ProductCategory
        fields = ["id", "Name", "Product"]

class ServiceProviderSerializer(ModelSerializer):
    User = UserModelSerializer(source="UserID", read_only=True)
    Product = ProductSerializer(source="ProductID")
    Gender = GenderSerializer(source="GenderID", read_only=True)
    class Meta:
        model = ServiceProvider
        fields = ["id", "User", "Product", "LocationID", "Gender", "AgeBracket", "WorkingDays"]

class RequestedServiceSerializer(ModelSerializer):
    Product = ProductSerializer(source="ProductID", read_only=True)
    User = UserModelSerializer(source="UserID", read_only=True)
    Location = TownsModelSerializer(source="LocationID", read_only=True)
    class Meta:
        model = ServiceRequest
        fields = ["id", "Product", "User", "Location", "Timestamp"]