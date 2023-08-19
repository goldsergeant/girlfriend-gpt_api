from django.urls import path
from chat.views import CharacterListView, SendMessageToCharacter

urlpatterns = [
    # path('charles/message/', SendMessageToCharlesfriendView.as_view(), name='boyfriend_message'),
    # path('mika/message/', SendMessageToMikaView.as_view(), name='girlfriend_message'),
    path('<int:character_id>/message/',SendMessageToCharacter.as_view(),name='character_message'),
    path('characters/', CharacterListView.as_view(),name='character_list')
]