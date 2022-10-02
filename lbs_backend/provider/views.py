from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import ProviderModel, ProviderService
from .serializers import (
    ProviderSerializer, ProviderServiceSerializer, CreateProviderServiceSerializer
)


class CreateProvider(APIView):
    pk = openapi.Parameter('pk', openapi.IN_QUERY,
                           description="Get Provider Details by primary key query param`(optional)`",
                           type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Request Provider Details <br> `(Optional)`  ->  Query_params: `pk` "
                                               "<br> or by Authenticated User",
                         tags=["Provider"], manual_parameters=[pk], responses={200: ProviderSerializer(many=False)})
    def get(self, request):
        if request.user:
            print("By Auth")
            provider_obj = ProviderModel.objects.filter(UserID_id=request.user.id).first()
            print(provider_obj)
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        if request.query_params["pk"]:
            print("By pk")
            provider_obj = ProviderModel.objects.filter(UserID_id=request.query_params["pk"]).first()
            return Response(ProviderSerializer(provider_obj, many=False).data, status.HTTP_200_OK)

        return Response({"data": "Provider"}, status=status.HTTP_200_OK)

    def post(self, request):
        post_data = request.data
        serializer = CreateProviderServiceSerializer(request.data)
        if serializer.is_valid():
            pass

