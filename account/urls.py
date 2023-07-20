from collections import OrderedDict

from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView,TokenObtainPairView
from account.views import UserSignupView, MyTokenObtainPairView, UserPasswordChangeView


schema_view = get_schema_view(openapi.Info(
    title="GirlfriendGPT API",
    default_version='v1',
    description="Test description",

),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('signin/',TokenObtainPairView.as_view()),
    path('signin/',MyTokenObtainPairView.as_view()),
    path('signup/', UserSignupView.as_view(),name='signup'),
    path('password/',UserPasswordChangeView.as_view(),name='change_password')
]
