from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from services.models import (
    ServiceProvider, ServiceRequest
)
from services.serializers.serializer_models import (
    ServiceProviderSerializer, RequestedServiceSerializer
)
from services.serializers.serializer_forms import (
    ServiceRequestCreationSerializer, CreateServiceProviderSerilizer
)


# Service Provider CRUD Endpoint

class ServiceProviderView(APIView):

    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)", type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)", type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for getting Service Providers response [you may pass all the query params]", manual_parameters=[ProviderID, ProductID, LocationID], responses={200: ServiceProviderSerializer(many=True)})
    def get(self, request):
        data = request.query_params
        if "ProviderID" in data:
            provider = ServiceProvider.objects.filter(id=data["ProviderID"])
            serializer = ServiceProviderSerializer(provider, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if "ProductID" in data and "LocationID" in data:
            provider = ServiceProvider.objects.filter(ProductID_id=data["ProductID"], LocationID_id=data["LocationID"])
            serializer = ServiceProviderSerializer(provider, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "ProductID" in data:
            provider = ServiceProvider.objects.filter(ProductID_id=data["ProductID"])
            serializer = ServiceProviderSerializer(provider, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if "LocationID" in data:
            provider = ServiceProvider.objects.filter(LocationID_id=data["LocationID"])
            serializer = ServiceProviderSerializer(provider, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        providers = ServiceProvider.objects.all()
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(operation_description="Endpoint for Service Providers Creation",
        request_body=CreateServiceProviderSerilizer,responses={200: ServiceProviderSerializer(many=False)}
    )
    def post(self, request):

        data = request.data
        serializer = CreateServiceProviderSerilizer(data=data)
        if serializer.is_valid():
            provider = ServiceProvider(UserID_id=data["UserID"], ProductID_id=data["ProductID"], LocationID_id=data["LocationID"])
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

class RequestServiceView(APIView):

    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID param(optional)", type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)", type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for Services Requests", manual_parameters=[UserID, ProductID, LocationID], responses={200: RequestedServiceSerializer(many=True)})
    def get(self, request, format=None):
        
        data = request.query_params

        if "ProductID" in data and "UserID" in data and "LocationID" in data:
            requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"], UserID_id=data["UserID"], LocationID_id=data["LocationID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if "ProductID" in data and "UserID" in data:
            requests = ServiceRequest.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if "LocationID" in data and "UserID" in data:
            requests = ServiceRequest.objects.filter(UserID_id=data["UserID"], LocationID_id=data["LocationID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "UserID" in data:
            requests = ServiceRequest.objects.filter(UserID_id=data["UserID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if "LocationID" in data:
            requests = ServiceRequest.objects.filter(LocationID_id=data["LocationID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if "ProductID" in data:
            requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"])
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        requests = ServiceRequest.objects.all()
        serializer = RequestedServiceSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body= ServiceRequestCreationSerializer,responses={201: RequestedServiceSerializer(many=False)}
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
