from collections import OrderedDict

from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView,TokenObtainPairView

from account import views

class CustomizedOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_paths(self, endpoints, components, request, public):
        if not endpoints:
            return openapi.Paths(paths={}), ''

        prefix = self.determine_path_prefix(list(endpoints.keys())) or ''
        assert '{' not in prefix, "base path cannot be templated in swagger 2.0"

        paths = OrderedDict()
        for path, (view_cls, methods) in sorted(endpoints.items()):
            operations = {}
            for method, view in methods:
                if not self.should_include_endpoint(path, method, view, public):
                    continue

                operation = self.get_operation(view, path, prefix, method, components, request)
                if operation is not None:
                    operations[method.lower()] = operation

            if operations:
                path_suffix = path[len(prefix):]
                if not path_suffix.startswith('/'):
                    path_suffix = '/' + path_suffix
                paths[path] = self.get_path_item(path, view_cls, operations)
                #  Only override this above line of upper level class paths[path_suffix] = ... to paths[path] = ...

        return self.get_paths_object(paths), prefix

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 로그인/회원가입
    # path('singin/', views.JWTLoginView.as_view()),
    # path('signup/', views.JWTSignupView.as_view()),
]
