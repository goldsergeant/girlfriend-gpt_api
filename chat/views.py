from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializer import SendMessageSerializer
from .chatbot import BoyfriendChatBot


# Create your views here.
class SendMessageView(APIView):

    @extend_schema(
        request=SendMessageSerializer
    )
    def post(self, request):
        serializer = SendMessageSerializer
        if serializer.is_valid(raise_exception=True):
            return Response(BoyfriendChatBot.send_message(message=request.data['content']))
        return Response(serializer.errors)