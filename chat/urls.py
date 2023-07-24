from django.urls import path
from chat.views import SendMessageView

urlpatterns = [
    path('boyfriend/message/', SendMessageView.as_view(),name='boyfriend_message')
]