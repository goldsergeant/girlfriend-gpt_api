from django.urls import path
from chat.views import SendMessageToBoyfriendView, SendMessageToGirlfriendView

urlpatterns = [
    path('boyfriend/message/', SendMessageToBoyfriendView.as_view(), name='boyfriend_message'),
    path('girlfriend/message/', SendMessageToGirlfriendView.as_view(), name='girlfriend_message')
]