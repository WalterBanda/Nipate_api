from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer
)


class CreateProvider(APIView):

    def get(self, request):
        if request.user:
            provider_obj = ProviderModel.objects.filter(UserID=request.user.id).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        if request.query_params["pk"]:
            provider_obj = ProviderModel.objects.filter(UserID_id=request.query_params["pk"]).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        return Response({"data": "Provider"}, status=status.HTTP_200_OK)
