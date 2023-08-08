import os
from json import JSONDecodeError

import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.base_user import BaseUserManager
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from account.models import User
from account.serializers import UserJWTSignupSerializer, MyTokenObtainPairSerializer, PasswordChangeSerializer, \
    UserInfoSerializer

BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'auth/google/callback/'
state = os.environ.get("STATE")


# Create your views here.
class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserJWTSignupSerializer,
        responses={201: UserJWTSignupSerializer},
    )
    def post(self, request):
        serializer = UserJWTSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # DB 저장
            return Response(serializer.data, status=201)


class UserNameUpdateView(APIView):
    @extend_schema(request=inline_serializer(
        name='UserJWTSigupSerializer',
        fields={
            'name': serializers.CharField()
        }
    ),
    )
    def put(self, request):
        serialzier = UserJWTSignupSerializer(data=request.data)
        user = request.user
        serialzier.update(instance=user, validated_data=request.data)
        return JsonResponse({'new_name': f'{user.name}'})


class UserPasswordChangeView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=PasswordChangeSerializer)
    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=request.data['email'])
            serializer.update(instance=user, validated_data=request.data)
            return JsonResponse({'messages': 'password is changed'}, status=200)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return JsonResponse({'messages': e.detail['detail']}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info(request):
    serializer = UserInfoSerializer(data={'email': request.user.email})
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=status.HTTP_200_OK)


from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view



class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")

    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        return JsonResponse({"error_message":error}, status=status.HTTP_400_BAD_REQUEST)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'error_message': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # return JsonResponse({'access': access_token, 'email':email})

    #################################################################

    # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        user = User.objects.get(email=email)

        social_user = SocialAccount.objects.get(user=user)

        # 있는데 구글계정이 아니어도 에러
        if social_user.provider != 'google':
            return JsonResponse({'error_message': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}auth/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        token=RefreshToken.for_user(user)
        response={}
        response['access']=str(token.access_token)
        response['refresh']=str(token)
        return JsonResponse(response)

    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}auth/google/login/finish/", data=data)
        accept_status = accept.status_code

        # social_user_info_scope='https://www.googleapis.com/auth/userinfo.profile'
        # social_user_info=requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}&scope={social_user_info_scope}")

        # 뭔가 중간에 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({'error_message': 'failed to signup'}, status=accept_status)

        user = User.objects.get(email=email)

        token = RefreshToken.for_user(user)
        response = {}
        response['access'] = str(token.access_token)
        response['refresh'] = str(token)
        return JsonResponse(response)
        # token=RefreshToken.for_user(user)
        # response={}
        # response['access_token'] = str(token.access_token)
        # response['refresh_token'] = str(token)
        # return JsonResponse(response)

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
        return JsonResponse({'error_message': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
