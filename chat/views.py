from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, mixins, generics
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Character
from chat.serializer import SendMessageSerializer, CharacterSerializer
from chat.chatbot import ChatBot


# Create your views here.
class SendMessageToCharacter(APIView):
    queryset = Character.objects.all()

    @extend_schema(
        request=inline_serializer(
            name='SendMessageSerializer',
            fields={
                'content': serializers.CharField()
            }
        )
    )
    def post(self, request, **kwargs):
        serializer = SendMessageSerializer(data=request.data)
        character = None
        try:
            character = self.queryset.get(id=kwargs['character_id'])
        except Character.DoesNotExist:
            return JsonResponse(
                {'error': 'cannot find character'}, status=404
            )
        chatbot = ChatBot(character=character)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse(
                {'message': chatbot.send_message(username=request.user.name, message=request.data['content'])})
        return Response(serializer.errors)


# class SendMessageToCharlesfriendView(APIView):
#     try:
#         charles = Character.objects.get(name='Charles')
#     except Character.DoesNotExist:
#         charles = None
#
#     @extend_schema(
#         request=inline_serializer(
#             name='SendMessageSerializer',
#             fields={
#                 'content': serializers.CharField()
#             }
#         )
#     )
#     def post(self, request):
#         serializer = SendMessageSerializer(data=request.data)
#         chatbot = ChatBot(character=self.charles)
#         if serializer.is_valid(raise_exception=True):
#             return JsonResponse(
#                 {'message': chatbot.send_message(username=request.user.name, message=request.data['content'])})
#         return Response(serializer.errors)
#
#
# class SendMessageToMikaView(APIView):
#     try:
#         mika = Character.objects.get(name='Mika')
#     except Character.DoesNotExist:
#         mika = None
#
#     @extend_schema(
#         request=inline_serializer(
#             name='SendMessageSerializer',
#             fields={
#                 'content': serializers.CharField()
#             }
#         )
#     )
#     def post(self, request):
#         serializer = SendMessageSerializer(data=request.data)
#         chatbot = ChatBot(character=self.mika)
#         if serializer.is_valid(raise_exception=True):
#             return JsonResponse(
#                 {'message': chatbot.send_message(username=request.user.name, message=request.data['content'])})
#         return Response(serializer.errors)


class CharacterListView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
