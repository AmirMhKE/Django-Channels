from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, room, registration, room_confirm

urlpatterns = [
    path('', home, name='home'),
    path('<str:room_name>/', room, name='room'),
    path('<str:room_name>/<slug:action_name>/confirm/', room_confirm, name='room_confirm'),
    path('auth/registration', registration, name='registration'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]