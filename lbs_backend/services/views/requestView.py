from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from services.models import (
    ProductCategory, Product, ServiceProvider, ServiceRequest
)
from services.serializers import (
    ProductCategorySerailizer, ProductSerializer, ServiceProviderSerializer, RequestedServiceSerializer
)

class ServiceProviderView(APIView):
    ID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)", type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for Providers get response", manual_parameters=[ID, ProductID], responses={200: ServiceProviderSerializer(many=True)})
    def get(self, request):
        try:
            try:
                dataID = request.query_parms['ProviderID']
                ProductID = request.query_parms['ProductID']
                try:
                    provider = ServiceProvider.objects.filter(id=dataID, ProductID_id=ProductID)
                    serializer = ServiceProviderSerializer(provider, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except ServiceProvider.DoesNotExist:
                    pass
            except:
                ProductID = request.query_parms['ProductID']
                try:
                    provider = ServiceProvider.objects.filter(ProductID_id=ProductID)
                    serializer = ServiceProviderSerializer(provider, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except ServiceProvider.DoesNotExist:
                    pass
        except:
            providers = ServiceProvider.objects.all()
            serializer = ServiceProviderSerializer(providers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        request_body=openapi.Schema(description="Create Service Provider Account=", type=openapi.TYPE_OBJECT,required=['UserID', 'ProductID'],
            properties={
                'UserID': openapi.Schema(description="UserID data", type=openapi.TYPE_INTEGER),
                'ProductID': openapi.Schema(description="ProductID data", type=openapi.TYPE_INTEGER),
                'LocationID': openapi.Schema(description="LocationID data(optional)", type=openapi.TYPE_INTEGER),
                'GenderID': openapi.Schema(description="GenderID data(optional)", type=openapi.TYPE_INTEGER),
                'AgeBracket': openapi.Schema(description="AgeBracket data(optional)", type=openapi.TYPE_STRING)
            }
        ),responses={200: ServiceProviderSerializer(many=False)}
    )
    def post(self, request):
        try:
            data = request.data
            provider = ServiceProvider(UserID=data["UserID"], ProductID=data["ProductID"])
            try:
                provider.LocationID = data["LocationID"]
            except:
                pass
            try:
                provider.GenderID = data["GenderID"]
            except:
                pass
            try:
                provider.AgeBracket = data["AgeBracket"]
            except:
                pass
            provider.save()
            serializer = ServiceProviderSerializer(provider, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestServiceView(APIView):

    UserID = openapi.Parameter('UserID', openapi.IN_QUERY, description="Get by UserID param(optional)", type=openapi.TYPE_INTEGER)
    ProductID = openapi.Parameter('ProductID', openapi.IN_QUERY, description="Get by ProductID param(optional)", type=openapi.TYPE_INTEGER)
    LocationID = openapi.Parameter('LocationID', openapi.IN_QUERY, description="Get by LocationID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for Services Requests", manual_parameters=[UserID, ProductID, LocationID], responses={200: RequestedServiceSerializer(many=True)})
    def get(self, request):
        try:
            data = request.query_params
            try:
                requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"], UserID_id=data["UserID"], LocationID_id=data["LocationID"])
                serializer = RequestedServiceSerializer(requests, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                pass
            try:
                requests = ServiceRequest.objects.filter(LocationID_id=data["LocationID"])
                serializer = RequestedServiceSerializer(requests, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                pass
            try:
                requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"])
                serializer = RequestedServiceSerializer(requests, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                pass
        except:
            requests = ServiceRequest.objects.all()
            serializer = RequestedServiceSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)