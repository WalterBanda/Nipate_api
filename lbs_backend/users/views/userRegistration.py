from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model
from ..serializers import UserModelSerializer, userRegistrationSerializer


User = get_user_model()

class userRegistration(APIView):

    @swagger_auto_schema(request_body=userRegistrationSerializer,responses={201: UserModelSerializer(many=False)})
    def post(self, request):
        data = request.data

        users = userRegistrationSerializer(data=data)
        if users.is_valid():
            user_number = User.objects.filter(MobileNumber=data["MobileNumber"]).first()
            if user_number:
                return Response({"Error": "User with MobileNumber already exists"}, status.HTTP_400_BAD_REQUEST)
            user_id_no = User.objects.filter(IDNumber=data["IDNumber"]).first()
            if user_id_no:
                return Response({"Error": "User with IDNumber already exists"}, status.HTTP_400_BAD_REQUEST)
            else:
                user = User(MobileNumber=data["MobileNumber"], IDNumber=data["IDNumber"], FirstName=data["FirstName"], SurName=data["LastName"])
                user.LocationID_id = data["LocationID"]
                user.GenderID_id = data["GenderID"]
                user.set_password(data["password"])
                try:
                    user.save()
                    serializer = UserModelSerializer(user, many=False)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response(
                        {"Error": ["Db LocationID or GenderID IntegrityError constraint failed"]},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        
        return Response(users.errors, status.HTTP_400_BAD_REQUEST)


    ID = openapi.Parameter('ID', openapi.IN_QUERY, description="get user by id param", type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(operation_description="Endpoint for getting user", manual_parameters=[ID], responses={200: UserModelSerializer(many=False)})
    def get(self, request):
        data = request.query_params
        if "ID" in data:
            user = User.objects.filter(id=data['ID']).first()
            if user is None:
                return Response({'Error': "User does not exists"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserModelSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({"Error": "please provide the ID param"}, status=status.HTTP_400_BAD_REQUEST)