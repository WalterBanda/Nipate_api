from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    ServiceCategory, Service, Advertisement
)
from .serializers import (
    ServiceCategorySerailizer, ServiceSerializer, InverseCategorySerializer, AdvertisementSerializer
)


# Product Views
class ServicesCategoryView(APIView):

    @swagger_auto_schema(tags=["Services"], operation_description='get all product categories',
                         responses={200: ServiceCategorySerailizer(many=True)})
    def get(self, request):
        obj = ServiceCategory.objects.all()

        serializer = ServiceCategorySerailizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServicesView(APIView):
    Name = openapi.Parameter('Name', openapi.IN_QUERY,
                             description='search by Name', type=openapi.TYPE_STRING)
    CategoryID = openapi.Parameter('CategoryID', openapi.IN_QUERY,
                                   description='search by CategoryID', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(tags=["Services"], operation_description='get products endpoint', manual_parameters=[CategoryID, Name],
                         responses={200: ServiceSerializer(many=True)})
    def get(self, request):
        data = request.query_params

        if 'CategoryID' in data:
            obj = Service.objects.filter(CategoryID_id=data['CategoryID'])
            serializer = ServiceSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if 'Name' in data:
            obj = Service.objects.filter(Name__contains=data['Name'])
            serializer = ServiceSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        obj = Service.objects.all()
        serializer = ServiceSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllServicesView(APIView):

    @swagger_auto_schema(tags=["Services"], operation_description="Endpoint for finding All services",
                         responses={200: InverseCategorySerializer(many=True)})
    def get(self, request):
        products = ServiceCategory.objects.all()

        serializer = InverseCategorySerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPagination(PageNumberPagination):
    page_size = 5

# Pagination with Swagger Sample
# @swagger_auto_schema(
#         operation_description="Endpoint for getting Service Providers response [you may pass all the query params]",
#         manual_parameters=[ProviderID, ProductID, LocationID],
#         responses={200: openapi.Response(
#             description='paginated Services Providers', schema=ServiceProviderSerializer(many=True)
#         )}, paginator=RequestPagination())


class AdvertisementView(APIView):
    @swagger_auto_schema(tags=["Services"], operation_description="Advertisement CRUD Endpoints",
                         responses={200: AdvertisementSerializer(many=True)})
    def get(self, request):
        ads_obj = Advertisement.objects.all()
        return Response(AdvertisementSerializer(ads_obj, many=True).data, status.HTTP_200_OK)