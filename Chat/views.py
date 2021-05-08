from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .models import Chat
import json

@login_required(login_url="login")
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(members=user)

    context = {
        "chat_rooms": chat_rooms
    }

    return render(request, "chat/index.html", context)

@login_required(login_url="login")
def room(request, room_name):
    user = request.user
    chat_model = Chat.objects.filter(room_name=room_name)

    if not chat_model.exists():
        if user.is_superuser:
            chat = Chat.objects.create(room_name=room_name)
            chat.members.add(user)
        else:
            return redirect("index")
    else:
        chat_model[0].members.add(user)

    username = request.user.username

    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }

    return render(request, "chat/room.html", context)