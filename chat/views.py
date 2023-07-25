from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.serializer import SendMessageSerializer
from .chatbot import BoyfriendChatBot, GirlfriendChatBot


# Create your views here.
class SendMessageToBoyfriendView(APIView):

    @extend_schema(
        request=inline_serializer(
            name='SendMessageSerializer',
            fields={
                'content': serializers.CharField()
            }
        )
    )
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse({'message':BoyfriendChatBot.send_message(username=request.user.name,message=request.data['content'])})
        return Response(serializer.errors)

class SendMessageToGirlfriendView(APIView):

    @extend_schema(
        request=inline_serializer(
            name='SendMessageSerializer',
            fields={
                'content': serializers.CharField()
            }
        )
    )
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse({'message':GirlfriendChatBot.send_message(username=request.user.name,message=request.data['content'])})
        return Response(serializer.errors)