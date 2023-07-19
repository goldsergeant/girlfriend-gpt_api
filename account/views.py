from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserJWTSignupSerializer


# Create your views here.
class UserSignupView(APIView):

    @swagger_auto_schema(request_body=UserJWTSignupSerializer)
    def post(self,request):
        serializer = UserJWTSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # DB 저장
            return Response(serializer.data, status=201)