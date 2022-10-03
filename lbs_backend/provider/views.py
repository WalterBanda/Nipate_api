from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer, CreateProviderServiceSerializer,
    CreateProviderSerializer
)


# Create or Register New Provider
class ProviderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Details <br> User request must be Authorized header",
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
            provider, _ = ProviderModel.objects.get_or_create(UserID=request.user, CountyID_id=request.data["CountyID"])
            return Response(ProviderSerializer(provider, many=False).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProviderServiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Services <br> User request must be Authorized header",
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
