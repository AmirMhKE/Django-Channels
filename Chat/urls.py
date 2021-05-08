from django.urls import path
from django.contrib.auth import views
from .views import index, room

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('login', views.LoginView.as_view(template_name="chat/login.html"), name='login'),
]