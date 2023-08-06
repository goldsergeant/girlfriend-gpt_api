from django.contrib import admin
from django.urls import path, include, re_path
from account.urls import schema_view
from account.views import GoogleLogin
from girlfriend_gpt import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("polls.urls")),
    path('auth/', include("account.urls")),
    path('auth/',include('allauth.urls')),
    path('chat/', include("chat.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        # Open API 자체를 조회 : json, yaml,
        path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
        path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
        # Open API Document UI로 조회: Swagger, Redoc
        path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui", ),
        path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc", ),
    ]
