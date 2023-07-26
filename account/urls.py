from collections import OrderedDict

from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView,TokenObtainPairView
from account.views import UserSignupView, MyTokenObtainPairView, UserPasswordChangeView, UserNameUpdateView, user_info, \
    GoogleLogin, google_login, google_callback

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
    path('password/',UserPasswordChangeView.as_view(),name='change_password'),
    path('user/name',UserNameUpdateView.as_view(),name='update_name'),
    path('user/info',user_info,name='get_user_info'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/',google_login,name='google_login'),
    path('google/login/finish/', GoogleLogin.as_view(),name='google_finish')
]
