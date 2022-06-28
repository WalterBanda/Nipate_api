from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from services.models import (
    RequestResponse
)
from services.serializers.serializer_models import (
    RequestResponseSerializer
)

class RequestedResponseView(APIView):

    ID = openapi.Parameter('ID', openapi.IN_QUERY, description="Get by ID param(optional)", type=openapi.TYPE_INTEGER)
    RequestID = openapi.Parameter('RequestID', openapi.IN_QUERY, description="Get by RequestID param(optional)", type=openapi.TYPE_INTEGER)
    ProviderID = openapi.Parameter('ProviderID', openapi.IN_QUERY, description="Get by ProviderID param(optional)", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for Services Requests", manual_parameters=[ID, RequestID, ProviderID], responses={200: RequestResponseSerializer(many=True)})
    def get(self, request):
        data = request.query_params
        try:
            try:
                response = RequestResponse.objects.filter(id=data["ID"], RequestID_id=data["RequestID"], ProviderID_id=data["ProviderID"])
                serializer = RequestResponseSerializer(response, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                pass
            if data["ID"] is not None:
                response = RequestResponse.objects.filter(id=data["ID"])
                serializer = RequestResponseSerializer(response, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            if data["RequestID"] is not None:
                response = RequestResponse.objects.filter(RequestID_id=data["RequestID"])
                serializer = RequestResponseSerializer(response, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            if data["ProviderID"] is not None:
                response = RequestResponse.objects.filter(ProviderID_id=data["id"])
                serializer = RequestResponseSerializer(response, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
        except:
            response = RequestResponse.objects.all()
            serializer = RequestResponseSerializer(response, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(description="Create Service request Response", type=openapi.TYPE_OBJECT,required=['RequestID', 'ProviderID'],
            properties={
                'RequestID': openapi.Schema(description="UserID", type=openapi.TYPE_INTEGER),
                'ProviderID': openapi.Schema(description="ProductID", type=openapi.TYPE_INTEGER),
                'ResponseText': openapi.Schema(description="ResponseText (optional)", type=openapi.TYPE_STRING),
            }
        ),responses={201: RequestResponseSerializer(many=False)}
    )
    def post(self, request):
        data = request.data
        try:
            if data["RequestID"] and data["ProviderID"] is not None:
                response = RequestResponse(RequestID_id=data["RequestID"], ProviderID_id=data["ProviderID"])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if data["ResponseText"] is not None:
                response.ResponseText = data["ResponseText"]
            response.save()
            serializer = RequestResponseSerializer(response, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)