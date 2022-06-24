from re import I
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from ..serializers import UserModelSerializer


User = get_user_model()

class userRegistration(APIView):

    def post(self, request):
        data = request.data

        if data['IDNumber'] is None:
            return Response({'Error': 'IDNumber is none'}, status.HTTP_400_BAD_REQUEST)
        if data['MobileNumber'] is None:
            return Response({'Error': 'MobileNumber is none'}, status.HTTP_400_BAD_REQUEST)
        if data['FirstName'] is None:
            return Response({'Error': 'FirstName is none'}, status.HTTP_400_BAD_REQUEST)
        if data['password'] is None:
            return Response({'Error': 'password is none'}, status.HTTP_400_BAD_REQUEST)
        
        user = User(IDNumber=data["IDNumber"], MobileNumber=data["MobileNumber"],FirstName=data["FirstName"])
        user.set_password(data["password"])
        user.save()

        serializer = UserModelSerializer(user, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        data = request.query_params

        if data['ID'] is not None:
            user = User.objects.filter(id=data['ID'])
            if user is None:
                return Response({'Error': "User does not exists"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserModelSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response({"Error": "please provide the ID param"})