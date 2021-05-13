from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, room_search, room_leave, room, registration, room_confirm

urlpatterns = [
    path('', home, name='home'),
    path('page/<int:page>/', home, name='home'),
    path('search/<str:search_name>/', room_search, name='room_search'),
    path('search/<str:search_name>/page/<int:page>/', room_search, name='room_search'),
    path('<str:room_name>/leave/', room_leave, name='room_leave'),
    path('<str:room_name>/', room, name='room'),
    path('<str:room_name>/<slug:action_name>/confirm/', room_confirm, name='room_confirm'),
    path('auth/registration', registration, name='registration'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]