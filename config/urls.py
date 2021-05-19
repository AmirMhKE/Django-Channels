from Chat.views import handler404
from django.contrib import admin
from django.urls import path, include

handler400 = "Chat.views.handler400"
handler403 = "Chat.views.handler403"
handler404 = "Chat.views.handler404"
handler500 = "Chat.views.handler500"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('Chat.urls')),
    path('api/', include('api.urls')),
]
