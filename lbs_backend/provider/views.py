from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer, CreatePostProviderServiceSerializer,
    CreateProviderSerializer, SearchCenterLocationSerializer, UserStatusSerializer,
    SearchServiceSerializer
)
from .crud import createProviderService, pinProviderServiceCenter
from locations.serializers import CenterLocationSerializer

User = get_user_model()


# Create or Register New Provider
class ProviderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Details <br> User request must be Authenticated with "
                                               "Token header",
                         tags=["Provider"], responses={200: ProviderSerializer(many=False)})
    def get(self, request):
        if request.user:
            provider_obj = ProviderModel.objects.filter(userID_id=request.user.id).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        return Response({"error": "User is not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=["Provider"], operation_description="Create New Provider Account",
                         request_body=CreateProviderSerializer(),
                         responses={201: UserStatusSerializer(many=False)})
    def post(self, request):
        serializer = CreateProviderSerializer(data=request.data)
        if serializer.is_valid():
            provider, _ = ProviderModel.objects.get_or_create(userID=request.user)
            provider.CountyID_id = request.data["countyID"]
            provider.save()

            details = {
                "id": provider.id,
                "user": {
                    "id": provider.userID.id,
                    "mobileNumber": provider.userID.mobileNumber,
                    "idNumber": provider.userID.idNumber,
                    "firstName": provider.userID.firstName,
                    "surName": provider.userID.surName
                },
                "location": {
                    "id": provider.countyID.id,
                    "name": provider.countyID.name
                },
                "provider": True
            }
            return Response(details, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProviderServiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Services <br> User request must be Authenticated with "
                                               "Token header",
                         tags=["Provider"], responses={200: ProviderServiceSerializer(many=True)})
    def get(self, request):
        if request.user:
            provider = ProviderModel.objects.filter(userID=request.user).first()
            if provider:
                services = ProviderService.objects.filter(providerID=provider)
                return Response(ProviderServiceSerializer(services, many=True).data, status.HTTP_200_OK)
            else:
                return Response({"error": "Provider Doesn't Exists"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Create Provider Service <br> User request must be Authenticated with "
                                               "Token header",
                         tags=["Provider"], request_body=CreatePostProviderServiceSerializer(),
                         responses={201: ProviderServiceSerializer(many=True)})
    def post(self, request):
        serializer = CreatePostProviderServiceSerializer(data=request.data)
        if serializer.is_valid():
            provider_id = ProviderModel.objects.filter(userID=request.user).first()
            if provider_id:
                provider_service = createProviderService(request.data, provider_id)
                return Response(ProviderServiceSerializer(provider_service, many=False).data, status.HTTP_201_CREATED)
            else:
                return Response({"error": "Provider Doesn't Exist"}, status.HTTP_404_NOT_FOUND)
            pass
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Services"], method="POST",
    operation_description="Search for services",
    request_body=SearchServiceSerializer,
    responses={200: ProviderServiceSerializer(many=True)}
)
@permission_classes([permissions.AllowAny])
@api_view(["POST"])
def searchProviderServices(request):
    data = request.data

    service_obj = ProviderService.objects.filter(
        Q(serviceTitle__icontains=data["searchdata"]) | Q(centerLocationID__DisplayName__icontains=data["searchdata"])
    )

    if data["serviceCategory"] != "" or data["serviceCategory"] is not None:
        service_obj = service_obj.filter(productID__CategoryID__Name__icontains=data["serviceCategory"])
    if data["region"] != "" or data["region"] is not None:
        service_obj = service_obj.filter(providerID__CountyID__Name__icontains=data["region"])

    return Response(ProviderServiceSerializer(service_obj, many=True).data, status.HTTP_200_OK)


@swagger_auto_schema(
    tags=["Provider"], method="POST",
    operation_description="Search Location where user is currently located at.",
    request_body=SearchCenterLocationSerializer(),
    responses={200: CenterLocationSerializer(many=False)}
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def searchCenterLocation(request):
    serializer = SearchCenterLocationSerializer(data=request.data)
    if serializer.is_valid():
        center = pinProviderServiceCenter(lattitude=request.data["lattitude"], longitude=request.data["longitude"])
        return Response(CenterLocationSerializer(center, many=False).data, status.HTTP_200_OK)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=['Provider'], method="GET", operation_description="Confirm If User is `Client/Provider`",
    responses={200: UserStatusSerializer(many=False)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def checkProviderStatus(request):
    if request.user:

        provider = ProviderModel.objects.filter(userID=request.user).first()
        if provider:
            details = {
                "id": provider.id,
                "user": {
                    "id": provider.userID.id,
                    "mobileNumber": provider.userID.mobileNumber,
                    "idNumber": provider.userID.idNumber,
                    "firstName": provider.userID.firstName,
                    "surName": provider.userID.surName
                },
                "location": {
                    "id": provider.countyID.id,
                    "name": provider.countyID.name
                },
                "provider": True
            }
            return Response(details, status.HTTP_200_OK)
        else:
            user = request.user
            details = {
                "id": user.id,
                "user": {
                    "id": user.id,
                    "mobileNumber": user.mobileNumber,
                    "idNumber": user.idNumber,
                    "firstName": user.firstName,
                    "surName": user.surName
                },
                "location": {
                    "id": user.locationID.id,
                    "Name": user.locationID.name
                },
                "provider": False
            }
            return Response(details, status.HTTP_200_OK)
    else:
        return Response({"message": "Credentials are invalid"}, status.HTTP_400_BAD_REQUEST)
