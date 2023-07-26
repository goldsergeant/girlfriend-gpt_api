import datetime

from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status, exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from django.contrib.auth import authenticate


User = get_user_model()


class UserJWTSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    name = serializers.CharField(
        required=False,
        write_only=True
    )

    subscription_date = serializers.DateField(
        required=False,
        write_only=True,
    )

    class Meta(object):
        model = User
        fields = ['email', 'password', 'name', 'subscription_date']

    def create(self, validated_data):
        user = User.objects.create(  # User 생성
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance

    def validate(self, validated_data):
        email = validated_data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise AuthenticationFailed(detail="user already exists")

        try:
            validate_email(email)

        except ValidationError:
            return JsonResponse({"message": "VALIDATION_ERROR"}, status=400)

        validated_data['subscription_date'] = datetime.date.today()

        return validated_data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise AuthenticationFailed(detail='user is not exist')
        elif authenticate(username=attrs['email'], password=attrs['password']) is None:
            raise AuthenticationFailed(detail='password is not valid')

        data = super().validate(attrs)

        # Add extra responses here
        return data

class PasswordChangeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        write_only=True
    )

    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type':'password'}
    )

    class Meta(object):
        model = User
        fields=['email','new_password','old_password']

    def update(self, instance:User, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    def validate(self, data):
        email = data.get('email', None)
        if not User.objects.filter(email=email).exists():
            raise AuthenticationFailed(detail="user is not exists")
        if not authenticate(username=data['email'],password=data['old_password']):
            raise ValidationError(detail='password is not correct')

        return data

class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )

    name =serializers.CharField(
        required=False
    )
    class Meta(object):
        model=User
        exclude=['password']

    def validate(self, attrs):
        email=attrs.get('email',None)
        if not User.objects.filter(email=email).exists():
            raise AuthenticationFailed(detail="user is not exists")

        return User.objects.get(email=email)