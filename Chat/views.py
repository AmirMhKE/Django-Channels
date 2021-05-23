import json
import re
import urllib

from account.forms import SignUpForm
from config import settings
from django.contrib.auth import (authenticate, get_user_model, login,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import redirect, render

from .models import Chat
from .persian_number_converter import convert


def handler400(request, exception=None):
    return redirect("home")

def handler403(request, exception=None):
    return redirect("home")

def handler404(request, exception):
    return redirect("home")

def handler500(request, exception=None):
    return redirect("home")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_case_insensitive_username(username):
    try:
        return get_user_model().objects.filter(username__iexact=username)[0].username
    except IndexError:
        return None

@login_required
def home(request, page=1):
    user = request.user
    chats = Chat.objects.filter(members=user)
    paginator = Paginator(chats, 5)

    try:
        chat_rooms = paginator.page(page)
    except EmptyPage:
        chat_rooms = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {
        "page": page,
        "main_url": "/chat/",
        "page_url": "/chat/page/",
        "paginator": paginator,
        "chat_rooms": chat_rooms,
        "type": "list"
    }

    return render(request, "chat/group_list.html", context)

@login_required
def room_search(request, search_name, page=1):
    chat_search = Chat.objects.filter(room_name__icontains=search_name)
    paginator = Paginator(chat_search, 5)
    
    try:
        chat_rooms = paginator.page(page)
    except EmptyPage:
        chat_rooms = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {
        "page": page,
        "main_url": f"/chat/search/{search_name}/",
        "page_url": f"/chat/search/{search_name}/page/",
        "paginator": paginator,
        "chat_rooms": chat_rooms,
        "search_name": search_name,
        "type": "search_list"
    }

    return render(request, "chat/group_list.html", context)

@login_required
def room(request, room_name):
    user = request.user
    chat_model = Chat.objects.filter(room_name=room_name)
    request_room_name = request.POST.get("room_name")
    request_action_name = request.POST.get("action_name")

    if request.method == "POST":
        if user.is_superuser and request_room_name == room_name and \
            request_action_name == "create" and not chat_model.exists():
            chat = Chat.objects.create(room_name=room_name)
            chat.members.add(user)
        elif request_room_name == room_name and request_action_name == "join" \
            and chat_model.exists():
            chat_model[0].members.add(user)
        else:
            return redirect("home")
    else:
        if not chat_model.exists():
            if user.is_superuser:
                return redirect("room_confirm", room_name=room_name, action_name="create")
            else:
                return redirect("home")
        elif chat_model.exists():
            if user not in chat_model[0].members.all():
                return redirect("room_confirm", room_name=room_name, action_name="join")
            else:
                pass

    username = request.user.username
    members_count = chat_model[0].members.count()

    context = {
        "room_name": room_name,
        "members_count": convert(members_count),
        "username": username,
    }

    return render(request, "chat/room.html", context)

@login_required
def room_leave(request, room_name):
    user = request.user
    chat = Chat.objects.filter(room_name=room_name)

    if chat.exists():
        if request.method == "POST":
            if user.is_superuser and request.POST.get("room_name") == room_name + "__delete":
                chat[0].delete()
                return redirect("home")

            if user in chat[0].members.all() and request.POST.get("room_name") == room_name:
                chat[0].members.remove(user)
        else:
            if user in chat[0].members.all():
                return redirect("room_confirm", room_name=room_name, action_name="leave")

    return redirect("home")

@login_required
def room_confirm(request, room_name, action_name):
    actions_list = ["join", "create", "leave"]
    if action_name not in actions_list:
        return redirect("home")

    user = request.user
    chat_model = Chat.objects.filter(room_name=room_name)

    context = {
        "chat": (lambda chat: chat_model[0] if chat.exists() else "")(chat_model),
        "room_name": room_name,
        "action_name": action_name,
        "username": request.user.username,
        "url": f"/chat/{room_name}/"
    }

    if chat_model.exists():
        if user in chat_model[0].members.all():
            if action_name == "join":
                return redirect("room", room_name=room_name)
            elif action_name == "leave":
                return render(request, "chat/room_leave_confirm.html", context)
        else:
            if action_name == "join":
                return render(request, "chat/room_confirm.html", context)
            elif action_name == "leave" and user.is_superuser:
                return render(request, "chat/room_leave_confirm.html", context)
    elif not chat_model.exists():
        if user.is_superuser and action_name == "create":
            return render(request, "chat/room_confirm.html", context)
        else:
            pass

    return redirect("home")

def username_validator(username):
    pattern = r"^[a-zA-Z]+([._]?[a-zA-Z0-9]+)*$"
    result = re.match(pattern, username)

    if result is None or len(username) < 5 or len(username) > 32:
        return False
    return True

def check_captcha(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    return result["success"]

def registration(request):
    if request.method == "POST":
        if not check_captcha(request):
            error_msg = "لطفا تیک من ربات نیستم را بزنید."
            form = {"errors": {"error": [error_msg]}}
            return render(request, 'chat/registration.html', {"form": form})

        if request.POST.get("submit") == "signup":
            ip = get_client_ip(request)
            data = request.POST.copy()
            data._mutable = True
            data.update({"username": data["username-signup"]})
            form = SignUpForm(data)
            ip_check = get_user_model().objects.filter(ip_address=ip)

            if ip_check:
                error_msg = "شما قبلا با این دستگاه یک اکانت ساخته اید و نمی توانید بیش از یک اکانت داشته باشید."
                form = {"errors": {"error": [error_msg]}}
                return render(request, 'chat/registration.html', {"form": form})

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                # Check CaseInsensitive
                check_user = get_case_insensitive_username(username)
                if check_user:
                    error_msg = "کاربری با آن نام کاربری وجود دارد."
                    form = {"errors": {"error": [error_msg]}}
                    return render(request, 'chat/registration.html', {"form": form})
                # End Check CaseInsensitive
                # Username Validate
                if not username_validator(username):
                    error_msg = "شما نمی توانید این نام کاربری را برای خود انتخاب کنید."
                    error_msg2 = "نام کاربری باید حداقل ۵ حرف و حداکثر ۳۲ حرف باشد و با حروف کوچک یا بزرگ انگلیسی شروع شود و بعد از آن می توانید از اعداد یا نقطه یا زیر خط استفاده کنید و همچنین نام کاربری باید با حروف انگلیسی کوچک یا بزرگ و یا اعداد تمام شود."
                    form = {"errors": {"error": [error_msg, error_msg2]}}
                    return render(request, 'chat/registration.html', {"form": form})
                # End Username Validate
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                get_user = get_user_model().objects.filter(username=username)[0]
                get_user.ip_address = ip
                get_user.save()
                return redirect('home')
            else:
                return render(request, 'chat/registration.html', {"form": form})
        elif request.POST.get("submit") == "login":
            username = request.POST.get("username-login")
            # CaseInsensitive
            username = get_case_insensitive_username(username)
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = "نام کاربری و یا رمز عبوری که وارد کردید اشتباه است."
                form = {"errors": {"error": [msg]}}
                return render(request, 'chat/registration.html', {"form": form})

    return render(request, "chat/registration.html")

@login_required
def user_update(request, username):
    user = get_user_model()
    # Check CaseInsensitive
    i_user = get_case_insensitive_username(username)
    if i_user and i_user != username:
        return redirect("user-update", username=get_case_insensitive_username(username))

    context = {
        "username": username
    }

    if username == request.user.username:
        if request.method == "POST":
            if request.POST.get("submit") == "change_username":
                form_username = request.POST.get("username")
                if form_username.replace(" ", "") and username_validator(form_username):
                    if not get_case_insensitive_username(form_username) or \
                    form_username.lower() == request.user.username.lower():
                        self_user = user.objects.get(username=username)
                        self_user.username = form_username
                        self_user.save()
                        return redirect("user-update", username=form_username)
            
                if not form_username.replace(" ", ""):
                    context.update({"username_error": "این مقدار لازم است."})
                elif not username_validator(form_username):
                    context.update({"username_error": "شما نمی توانید این نام کاربری را برای خود انتخاب کنید."})
                else:
                    context.update({"username_error": "این نام کاربری وجود دارد."})
            else:
                # change password
                password_change_form = PasswordChangeForm(request.user, request.POST)
                context.update({"form": password_change_form})
                if password_change_form.is_valid():
                    self_user = password_change_form.save()
                    update_session_auth_hash(request, self_user)
                    context.update({"password_changed": True})
        
        return render(request, "chat/user_update.html", context)

    return redirect("home")

@login_required
def delete_account(request, username):
    if request.user.username == username:
        if request.method == "POST":
            if request.POST.get("user") == username:
                user = get_user_model().objects.get(username=username)
                user.delete()
                return redirect("registration")

        return render(request, "chat/remove_account_confirm.html")

    return redirect("home")
