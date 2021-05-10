from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Chat
from .forms import SignUpForm
import json

@login_required(login_url="registration")
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(members=user)

    context = {
        "chat_rooms": chat_rooms
    }

    return render(request, "chat/index.html", context)

@login_required(login_url="registration")
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

def registration(request):
    if request.method == "POST":
        if request.POST.get("submit") == "signup":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'chat/registration.html', {"form": form})
        elif request.POST.get("submit") == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                msg = "نام کاربری و یا رمز عبوری که وارد کردید اشتباه است"
                form = {"errors": {"error": [msg]}}
                return render(request, 'chat/registration.html', {"form": form})

    return render(request, "chat/registration.html")