import datetime

from rest_framework import serializers
from rest_framework_jwt.serializers import User
from django.core.validators import validate_email


class UserJWTSignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    subscription_date = serializers.DateField(
        required=False,
        write_only=True,
    )

    class Meta(object):
        model = User
        fields = ['email', 'password', 'subscription_date']

    def save(self, request):
        user = User()

        user.email = self.validated_data['id']
        user.subscription_date = self.validated_data['subscription_date']

        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user already exists")

        if not validate_email(email):
            raise serializers.ValidationError("email is invalid")

        data['subscription_date'] = datetime.date.today()

        return data