from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse

from account.models import User
from account.serializers import UserJWTSignupSerializer, MyTokenObtainPairSerializer,PasswordChangeSerializer,UserInfoSerializer


# Create your views here.
class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserJWTSignupSerializer,
        responses={201: UserJWTSignupSerializer},
    )
    def post(self,request):
        serializer = UserJWTSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # DB 저장
            return Response(serializer.data, status=201)

class UserNameUpdateView(APIView):
    @extend_schema(request=UserJWTSignupSerializer)
    def put(self,request):
        serialzier=UserJWTSignupSerializer(data=request.data)
        user=request.user
        serialzier.update(instance=user,validated_data=request.data)
        return JsonResponse({'new_name':f'{user.name}'})
class UserPasswordChangeView(APIView):
    permission_classes=[AllowAny]

    @extend_schema(request=PasswordChangeSerializer)
    def put(self,request):
        serializer=PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=User.objects.get(email=request.data['email'])
            serializer.update(instance=user,validated_data=request.data)
            return JsonResponse({'messages':'password is changed'},status=200)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return JsonResponse({'messages':e.detail['detail']},status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info(request):
    serializer=UserInfoSerializer(data={'email':request.user.email})
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data,status=status.HTTP_200_OK)
