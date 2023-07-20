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


class SignupTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('signup')  # Replace 'signup' with the name of your signup view in urlpatterns
        self.valid_data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
        }

    def test_signup_success(self):
        response = self.client.post(
            self.url,
            data=self.valid_data,
            format='json',
        )
        # Check the response status code
        self.assertEqual(response.status_code, 201)
        # Check the user count in the database
        self.assertEqual(User.objects.count(), 1)

        # Check if the user is created with the correct username
        created_user = User.objects.get(email=self.valid_data['email'])
        self.assertIsNotNone(created_user)

    def test_signup_fail_email_invalid(self):
        data = self.valid_data.copy()
        data['email']='testexample.com'
        response = self.client.post(
            self.url,
            data=data,
            format='json'
        )
        # Check the response status code
        self.assertEqual(response.status_code, 400)

        # Check the user count in the database
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)

    def test_signup_in_already_exist(self):
        user=User(email=self.valid_data['email'])
        user.save()

        response = self.client.post(
            self.url,
            data=self.valid_data,
            format='json'
        )

        self.assertEqual(response.status_code,401)
        self.assertEqual(User.objects.count(),1)
