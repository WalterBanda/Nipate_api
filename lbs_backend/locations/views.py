from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from locations.models import TownsModel, CountyModel
from locations.serializers import TownsModelSerializer, CountyModelSerializers


class CountyView(APIView):

    def get(self, request):
        counties = CountyModel.objects.all()
        serializer = CountyModelSerializers(counties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TownsView(APIView):

    def get(self, request):
        towns = TownsModel.objects.all()
        serializer = TownsModelSerializer(towns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
