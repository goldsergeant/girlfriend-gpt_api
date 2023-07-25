from datetime import datetime

from rest_framework import serializers

from chat.models import Message




class SendMessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = ['content']

    def validate(self, attrs) -> str:
        content: str = attrs.get('content', None)

        if len(content) == 0:
            raise serializers.ValidationError(detail='content is required')

        return attrs
