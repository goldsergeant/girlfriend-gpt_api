from django.urls import path
from chat.views import SendMessageToCharlesfriendView, SendMessageToMikaView

urlpatterns = [
    path('charles/message/', SendMessageToCharlesfriendView.as_view(), name='boyfriend_message'),
    path('mika/message/', SendMessageToMikaView.as_view(), name='girlfriend_message')
]