from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import CountyModel, CenterLocation
from .serializers import CountyModelSerializers, CenterLocationSerializer


class CountyView(APIView):

    @swagger_auto_schema(operation_description="Endpoint for getting counties",
                         responses={200: CountyModelSerializers(many=True)})
    def get(self, request):
        counties = CountyModel.objects.all()
        serializer = CountyModelSerializers(counties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)