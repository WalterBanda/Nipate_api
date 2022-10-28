from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema, OrderedDict
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.http import FileResponse

from .serializers import (
    UserModelSerializer, LoginResponseSerializer, CreateAuthToken,
    userDetailsValidationSerializer, userPutDetailSerializer, AllDetailSerializer
)

User = get_user_model()


# App site favicon
@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request):
    file = (settings.BASE_DIR / "statics" / "favicon.png").open("rb")
    return FileResponse(file)


class UserRegister(APIView):

    @swagger_auto_schema(tags=['User'],
                         operation_description='Create new user using Mobile Number, Id/Passport number, First name & '
                                               'Last name',
                         request_body=userDetailsValidationSerializer, responses={201: UserModelSerializer(many=False)})
    def post(self, request):
        data = request.data
        if data:
            validate = userDetailsValidationSerializer(data=data)
            if validate.is_valid():
                valid_number = User.objects.filter(MobileNumber=data['mobileNumber'])
                if valid_number:
                    return Response({'error': 'User with number already exist'}, status.HTTP_400_BAD_REQUEST)

                user = User(**data)
                user.save()
                serializer = UserModelSerializer(user, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'please post required data'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['User'],
        operation_description='Update user details with: <br> -> Password <br> -> Location (From Counties list id: '
                              '`/location/counties/`) <br> -> Gender id.[Male: 1, Female: 2]',
        request_body=userPutDetailSerializer, responses={201: LoginResponseSerializer(many=False)}
    )
    def put(self, request):
        data = request.data
        validate = userPutDetailSerializer(data=data)
        if validate.is_valid():
            user = User.objects.filter(id=data['userID']).first()
            print(user)
            if user:
                user.genderID_id = data['genderID']
                user.locationID_id = data['locationID']
                user.set_password(data['password'])
                user.save()
                token, _ = Token.objects.get_or_create(user=user)

                results = LoginResponseSerializer({
                    "mobileNumber": user.mobileNumber, "firstName": user.firstName, "lastName": user.surName,
                    "auth_token": 'Token ' + token.key
                }, many=False)

                return Response(results.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(validate.errors, status=status.HTTP_400_BAD_REQUEST)


# Login views


def postUserLogin(data):
    user = User.objects.filter(MobileNumber=data["mobileNumber"]).first()

    if user:
        if user.check_password(data["password"]):
            return user
        else:
            return {"error": ["Invalid user credentials"]}
    else:
        return {"error": ["User not found"]}


class LoginJwtToken(APIView):

    @swagger_auto_schema(tags=['User'], operation_description="Get JWT token Header",
                         request_body=CreateAuthToken,
                         responses={200: LoginResponseSerializer(many=False)}
                         )
    def post(self, request):
        post_data = request.data
        serializer = CreateAuthToken(data=post_data)
        if serializer.is_valid():
            user = postUserLogin(post_data)
            try:
                token, _ = Token.objects.get_or_create(user_id=user.id)
                results = LoginResponseSerializer({
                    "mobileNumber": user.mobileNumber, "firstName": user.firstName, "lastName": user.surName,
                    "auth_token": 'Token ' + token.key
                }, many=False)
                return Response(results.data, status.HTTP_200_OK)

            except:
                return Response(user, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LogOutJwtToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    response = openapi.Schema('User', openapi.IN_BODY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(tags=['User'], operation_description="Delete JWT token Header",
                         responses={200: response}
                         )
    def post(self, request):
        print(request.user)
        request.user.auth_token.delete()
        return Response({"user": "succesfully log out"}, status.HTTP_200_OK)


# Request User details

class FetchUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=['User'],
                         operation_description="Get All  `Me`  Details <br> * User must be Authenticated",
                         responses={200: AllDetailSerializer(many=False)}
                         )
    def get(self, request):
        if request.user:
            return Response(AllDetailSerializer(request.user, many=False).data, status.HTTP_200_OK)
        else:
            return Response({"error": "User not Authenticated"}, status.HTTP_401_UNAUTHORIZED)


class ConfirmUser(APIView):

    @swagger_auto_schema(tags=['User'],
                         operation_description="Confirm If User Credentials is Valid",
                         responses={
                             200: openapi.Schema(type=openapi.TYPE_BOOLEAN, enum=[{"user": True}])
                         }
                         )
    def get(self, request):
        if request.user:
            token = Token.objects.filter(user=request.user).first()
            if token:
                return Response({"user": True}, status.HTTP_200_OK)
            else:
                return Response({"user": False}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"user": False}, status.HTTP_404_NOT_FOUND)
