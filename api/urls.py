from django.urls import path
from .views import ChatList

urlpatterns = [
    path('chats/', ChatList.as_view({"get": "chat_lists"}), name='chat-list'),
]