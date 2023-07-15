from rest_framework import serializers

from girlfriend_gpt.girlfriend.models import GirlfriendResponse


class GirlfriendSerializer(serializers.ModelSerializer):
    # ModelSerializer 를 이용해서 아래와 같이 짧은 코드로 직렬화 필드를 정의할 수 있다
    class Meta:
        model = GirlfriendResponse
        fields = ('created', 'content')

        # 신규 Bbs instance를 생성해서 리턴해준다

    def create(self, validated_data):
        return GirlfriendResponse.objects.create(**validated_data)

        # 생성되어 있는 Bbs instance 를 저장한 후 리턴해준다

    def update(self, instance, validated_data):
        instance.created = validated_data.get('created',instance.created)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance