from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi

# from account.urls import CustomizedOpenAPISchemaGenerator
from girlfriend_gpt import settings
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(openapi.Info(
    title="GirlfriendGPT API",
    default_version='v1',
    description="Test description",

),
    public=True,
    # generator_class=CustomizedOpenAPISchemaGenerator,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("polls.urls")),
    path('auth/', include("account.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
