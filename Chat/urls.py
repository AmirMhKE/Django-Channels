from django.urls import path
from .views import index, room, registration

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('auth/registration', registration, name='registration')
]