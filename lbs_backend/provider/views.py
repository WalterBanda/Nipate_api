from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth import get_user_model
from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer, CreatePostProviderServiceSerializer,
    CreateProviderSerializer, SearchCenterLocationSerializer, UserStatusSerializer
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
            provider_obj = ProviderModel.objects.filter(UserID_id=request.user.id).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        return Response({"Error": "User is not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=["Provider"], operation_description="Create New Provider Account",
                         request_body=CreateProviderSerializer(),
                         responses={201: ProviderSerializer(many=False)})
    def post(self, request):
        serializer = CreateProviderSerializer(data=request.data)
        if serializer.is_valid():
            provider, _ = ProviderModel.objects.get_or_create(UserID=request.user)
            provider.CountyID_id = request.data["CountyID"]
            provider.save()
            return Response(ProviderSerializer(provider, many=False).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProviderServiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Services <br> User request must be Authenticated with "
                                               "Token header",
                         tags=["Provider"], responses={200: ProviderServiceSerializer(many=True)})
    def get(self, request):
        if request.user:
            provider = ProviderModel.objects.filter(UserID=request.user).first()
            if provider:
                services = ProviderService.objects.filter(ProviderID=provider)
                return Response(ProviderServiceSerializer(services, many=True).data, status.HTTP_200_OK)
            else:
                return Response({"Error": "Provider Doesn't Exists"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Create Provider Service <br> User request must be Authenticated with "
                                               "Token header",
                         tags=["Provider"], request_body=CreatePostProviderServiceSerializer(),
                         responses={201: ProviderServiceSerializer(many=True)})
    def post(self, request):
        serializer = CreatePostProviderServiceSerializer(data=request.data)
        if serializer.is_valid():
            provider_id = ProviderModel.objects.filter(UserID=request.user).first()
            if provider_id:
                provider_service = createProviderService(request.data, provider_id)
                return Response(ProviderServiceSerializer(provider_service, many=False).data, status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Provider Doesn't Exist"}, status.HTTP_404_NOT_FOUND)
            pass
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Provider"], method="POST",
    operation_description="Search Location where user is currently located at.",
    request_body=SearchCenterLocationSerializer(),
    responses={200: CenterLocationSerializer(many=False)}
)
@api_view(["POST"])
def searchCenterLocation(request):
    serializer = SearchCenterLocationSerializer(data=request.data)
    if serializer.is_valid():
        center = pinProviderServiceCenter(lattitude=request.data["Lattitude"], longitude=request.data["Longitude"])
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

        provider = ProviderModel.objects.filter(UserID=request.user).first()
        if provider:
            details = {
                "id": provider.id,
                "User": {
                    "id": provider.UserID.id,
                    "MobileNumber": provider.UserID.MobileNumber,
                    "IDNumber": provider.UserID.IDNumber,
                    "FirstName": provider.UserID.FirstName,
                    "SurName": provider.UserID.SurName
                },
                "Location": {
                    "id": provider.CountyID.id,
                    "Name": provider.CountyID.Name
                },
                "Provider": True
            }
            return Response(details, status.HTTP_200_OK)
        else:
            user = request.user
            details = {
                "id": user.id,
                "User": {
                    "id": user.id,
                    "MobileNumber": user.MobileNumber,
                    "IDNumber": user.IDNumber,
                    "FirstName": user.FirstName,
                    "SurName": user.SurName
                },
                "Location": {
                    "id": user.LocationID.id,
                    "Name": user.LocationID.Name
                },
                "Provider": False
            }
            return Response(details, status.HTTP_200_OK)
    else:
        return Response({"message": "Credentials are invalid"}, status.HTTP_400_BAD_REQUEST)
