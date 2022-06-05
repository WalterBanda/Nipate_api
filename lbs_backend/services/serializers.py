from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .models import (
    WorkingDays, ProductCategory, Product, ServiceProvider
)
from users.serializers import UserModelSerializer, GenderSerializer

class WorkingDaySerializer(ModelSerializer):

    class Meta:
        model = WorkingDays
        fields = ["days"]

class ProductCategorySerailizer(ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(ModelSerializer):
    Category = ProductCategorySerailizer(source="CategoryID", read_only=True)
    class Meta:
        model = Product
        fields = ["id", "Name", "Category"]

class ServiceProviderSerializer(ModelSerializer):
    User = UserModelSerializer(source="UserID", read_only=True)
    Product = ProductSerializer(source="ProductID")
    Gender = GenderSerializer(source="GenderID", read_only=True)
    class Meta:
        model = ServiceProvider
        fields = ["id", "User", "Product", "LocationID", "Gender", "AgeBracket", "WorkingDays"]
