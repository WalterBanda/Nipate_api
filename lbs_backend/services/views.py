from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    ProductCategory, Product, Advertisement, ServiceProvider, ServiceRequest,
    RequestResponse
)
from .serializers.serializer_models import (
    ProductCategorySerailizer, ProductSerializer, InverseCategorySerializer,
    AdvertisementSerializer, ServiceProviderSerializer, RequestedServiceSerializer,
    RequestResponseSerializer
)
from .serializers.serializer_forms import (
    CreateServiceProviderSerilizer, ServiceRequestCreationSerializer,
    ServiceResponseCreationSerializer
)
from .crud.requestsCrud import (get_services_requests, get_service_providers)


# Create Provider
class CreateProvider(APIView):

    def post(self, request):
        pass


# Product Views
class productCategoryView(APIView):

    @swagger_auto_schema(operation_description='get all product categories',
                         responses={200: ProductCategorySerailizer(many=True)})
    def get(self, request):
        obj = ProductCategory.objects.all()

        serializer = ProductCategorySerailizer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class productsView(APIView):
    Name = openapi.Parameter('Name', openapi.IN_QUERY,
                             description='search by Name', type=openapi.TYPE_STRING)
    CategoryID = openapi.Parameter('CategoryID', openapi.IN_QUERY,
                                   description='search by CategoryID', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description='get products endpoint', manual_parameters=[CategoryID, Name],
                         responses={200: ProductSerializer(many=True)})
    def get(self, request):
        data = request.query_params

        if 'CategoryID' in data:
            obj = Product.objects.filter(CategoryID_id=data['CategoryID'])
            serializer = ProductSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if 'Name' in data:
            obj = Product.objects.filter(Name__contains=data['Name'])
            serializer = ProductSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        obj = Product.objects.all()
        serializer = ProductSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllProductsView(APIView):

    @swagger_auto_schema(operation_description="Endpoint for finding All services",
                         responses={200: InverseCategorySerializer(many=True)})
    def get(self, request):
        products = ProductCategory.objects.all()

        serializer = InverseCategorySerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Advertisement Views
class AdvertView(APIView):
    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID id param(optional)",
                               type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID id param(optional)",
                                  type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID id param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Endpoint for requesting and serching ads",
                         manual_parameters=[UserID, ProductID, LocationID],
                         responses={200: AdvertisementSerializer(many=True)})
    def get(self, request):
        data = request.query_params
        if data["UserID"] and data["ProductID"] and data["LocationID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"],
                                                   LocationID_id=data["LocationID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["UserID"] and data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["LocationID"] and data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(LocationID_id=data["LocationID"], ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["UserID"] is not None:
            adverts = Advertisement.objects.filter(UserID_id=data["UserID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["ProductID"] is not None:
            adverts = Advertisement.objects.filter(ProductID_id=data["ProductID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if data["LocationID"] is not None:
            adverts = Advertisement.objects.filter(LocationID_id=data["LocationID"])
            serializer = AdvertisementSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        adverts = Advertisement.objects.all()
        serializer = AdvertisementSerializer(adverts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(description="Create an AD as a User", type=openapi.TYPE_OBJECT, required=['UserID'],
                                    properties={
                                        'UserID': openapi.Schema(description="UserID id", type=openapi.TYPE_INTEGER),
                                        'ProductID': openapi.Schema(description="ProductID id",
                                                                    type=openapi.TYPE_INTEGER),
                                        'LocationID': openapi.Schema(description="LocationID id(optional)",
                                                                     type=openapi.TYPE_INTEGER),
                                        'ADText': openapi.Schema(description="ADText text(optional)",
                                                                 type=openapi.TYPE_STRING),
                                        'GenderID': openapi.Schema(description="To target gender(optional)",
                                                                   type=openapi.TYPE_INTEGER),
                                        'ExpiryDate': openapi.Schema(
                                            description="Expires on certain datetime(optional)",
                                            type=openapi.TYPE_STRING),
                                        'NoOfMessages': openapi.Schema(description="Send this number of ADs(optional)",
                                                                       type=openapi.TYPE_INTEGER),
                                    }
                                    ), responses={201: AdvertisementSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        if data["UserID"] is not None:
            advert = Advertisement(UserID_id=data["UserID"])
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if data["ProductID"] is not None:
            advert.ProductID_id = data["ProductID"]
        if data["LocationID"] is not None:
            advert.LocationID_id = data["LocationID"]
        if data["ADText"] is not None:
            advert.ADText = data["ADText"]
        if data["GenderID"] is not None:
            advert.GenderID_id = data["GenderID"]
        if data["ExpiryDate"] is not None:
            try:
                advert.ExpiryDate = data["ExpiryDate"]
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if data["NoOfMessages"] is not None:
            advert.NoOfMessages = data["NoOfMessages"]
        advert.save()
        serializer = AdvertisementSerializer(advert, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Request views


class RequestPagination(PageNumberPagination):
    page_size = 5


# Service Provider CRUD Endpoint

class ServiceProviderView(APIView, RequestPagination):
    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)",
                                   type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)",
                                  type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description="Endpoint for getting Service Providers response [you may pass all the query params]",
        manual_parameters=[ProviderID, ProductID, LocationID],
        responses={200: openapi.Response(
            description='paginated Services Providers', schema=ServiceProviderSerializer(many=True)
        )}, paginator=RequestPagination())
    def get(self, request):
        data = request.query_params
        providers = get_service_providers(data)
        providers = self.paginate_queryset(providers, request, view=self)

        serializer = RequestedServiceSerializer(providers, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(operation_description="Endpoint for Service Providers Creation",
                         request_body=CreateServiceProviderSerilizer,
                         responses={200: ServiceProviderSerializer(many=False)}
                         )
    def post(self, request):

        data = request.data
        serializer = CreateServiceProviderSerilizer(data=data)
        if serializer.is_valid():
            provider = ServiceProvider(UserID_id=data["UserID"], ProductID_id=data["ProductID"],
                                       LocationID_id=data["LocationID"])
            if data["GenderID"] is not None:
                provider.GenderID_id = data["GenderID"]
            if data["AgeBracket"] is not None:
                provider.AgeBracket = data["AgeBracket"]
            try:
                provider.save()
                serializer = ServiceProviderSerializer(provider, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db UserID or ProductID or LocationID or GenderID IntegrityError constraint failed"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Services CRUD Endpoint
class RequestServiceView(APIView, RequestPagination):
    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID param(optional)",
                               type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)",
                                  type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Endpoint for Services Requests",
                         manual_parameters=[UserID, ProductID, LocationID],
                         responses={200: openapi.Response(
                             description='paginated Services Requests', schema=RequestedServiceSerializer(many=True)
                         )}, paginator=RequestPagination())
    def get(self, request):

        data = request.query_params
        requests = get_services_requests(data)
        requests = self.paginate_queryset(requests, request, view=self)

        serializer = RequestedServiceSerializer(requests, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=ServiceRequestCreationSerializer, responses={201: RequestedServiceSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        serializer = ServiceRequestCreationSerializer(data=data)
        if serializer.is_valid():
            requests = ServiceRequest(
                ProductID_id=data["ProductID"], UserID_id=data["UserID"], LocationID_id=data["LocationID"]
            )
            if data["RequestText"] is not None:
                requests.RequestText = data["RequestText"]
            try:
                requests.save()
                serializer = RequestedServiceSerializer(requests, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db ProductID or UserID or LocationID IntegrityError constraint failed"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Response Views

class RequestedResponseView(APIView):
    ResponseID = openapi.Parameter('ResponseID', openapi.IN_QUERY, description="Get by ResponseID param(optional)",
                                   type=openapi.TYPE_INTEGER)
    RequestID = openapi.Parameter('RequestID', openapi.IN_QUERY, description="Get by RequestID param(optional)",
                                  type=openapi.TYPE_INTEGER)
    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)",
                                   type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Endpoint for filtering Service responses by either params or All*",
                         manual_parameters=[ResponseID, RequestID, ProviderID],
                         responses={200: RequestResponseSerializer(many=True)})
    def get(self, request):

        data = request.query_params
        if "ResponseID" in data:
            response = RequestResponse.objects.filter(id=data["ResponseID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        if "RequestID" in data:
            response = RequestResponse.objects.filter(RequestID_id=data["RequestID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        if "ProviderID" in data:
            response = RequestResponse.objects.filter(ProviderID_id=data["ProviderID"])
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        response = RequestResponse.objects.all()
        serializer = RequestResponseSerializer(response, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ServiceResponseCreationSerializer, responses={201: RequestResponseSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        serializer = ServiceResponseCreationSerializer(data=data)
        if serializer.is_valid():
            response = RequestResponse(RequestID_id=data["RequestID"], ProviderID_id=data["ProviderID"])
            if data["ResponseText"] is not None:
                response.ResponseText = data["ResponseText"]
            try:
                response.save()
                serializer = RequestResponseSerializer(response, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"Error": ["Db RequestID or ProviderID IntegrityError constraint failed"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
