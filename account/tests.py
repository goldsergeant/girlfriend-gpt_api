import json

from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.
from rest_framework_simplejwt.tokens import AccessToken

# myapp/tests.py
import json
from django.test import TestCase
from django.urls import reverse

from account.models import User


class SignupTestCase(TestCase):
    def setUp(self):
        self.url = reverse('signup')  # Replace 'signup' with the name of your signup view in urlpatterns
        self.valid_data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
        }

    def test_signup_success(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_data),
            content_type='application/json',
        )
        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Check the user count in the database
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        # Check if the user is created with the correct username
        created_user = User.objects.get(username=self.valid_data['username'])
        self.assertIsNotNone(created_user)

    def test_signup_fail_email_invalid(self):
        data = self.valid_data.copy()
        data['password_confirm'] = 'wrongpassword'
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json',
        )
        # Check the response status code
        self.assertEqual(response.status_code, 400)

        # Check the user count in the database
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)

    # 여기에 추가 실패 테스트 케이스를 작성하세요.
    # (예: 사용자 이름이 없는 경우, 이미 사용 중인 이메일, 등록하지 않은 항목 등)
