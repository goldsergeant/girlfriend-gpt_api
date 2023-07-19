import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import User
from django.core.validators import validate_email

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
        required=False
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
            raise serializers.ValidationError("user already exists")

        try:
            validate_email(email)

        except ValidationError:
            return JsonResponse({"message": "VALIDATION_ERROR"}, status=400)

        validated_data['subscription_date'] = datetime.date.today()

        return validated_data

