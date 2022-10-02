from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer, CreateProviderServiceSerializer,
    CreateProviderSerializer
)


class CreateProvider(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Request Provider Details <br> User request must be Authorized header",
                         tags=["Provider"], responses={200: ProviderSerializer(many=False)})
    def get(self, request):
        if request.user:
            provider_obj = ProviderModel.objects.filter(UserID_id=request.user.id).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        return Response({"Error": "User is not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(tags=["Provider"], operation_description="Create New Provider Account", request_body=CreateProviderSerializer(),
                         responses={201: ProviderSerializer(many=False)})
    def post(self, request):
        serializer = CreateProviderServiceSerializer(request.data)
        if serializer.is_valid():
            provider, _ = ProviderModel.objects.get_or_create(UserID=request.user, CountyID_id=request.data["CountyID"])
            return Response(ProviderSerializer(provider, many=False).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
