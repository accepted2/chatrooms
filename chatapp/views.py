from django.shortcuts import get_object_or_404, redirect, render
from .models import Chatroom, ChatMessage
from .forms import RegisterForm, CreateRoomForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("register")
    if request.method == "POST":
        print(request.POST)
        form = CreateRoomForm(request.POST)

        if form.is_valid():

            form.save()
            return redirect("index")

    form = CreateRoomForm()
    chatrooms = Chatroom.objects.all()
    print(chatrooms)
    return render(
        request,
        "chatapp/index.html",
        {"chatrooms": chatrooms, "form": form},
    )


@login_required(login_url="login")
def chatroom(request, slug, room_id):
    # chatroom = Chatroom.objects.get(slug=slug)
    chatrooms = Chatroom.objects.all()
    chatroom = get_object_or_404(Chatroom, id=room_id)
    messages = ChatMessage.objects.filter(room=chatroom)
    users = chatroom.get_users()

    return render(
        request,
        "chatapp/room.html",
        {
            "chatroom": chatroom,
            "messages": messages,
            "users": users,
            "chatrooms": chatrooms,
        },
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration is complete!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "chatapp/register.html", {"form": form})


# Для логина используем стандартное представление
class CustomLoginView(LoginView):
    template_name = "chatapp/login.html"


def logoutUser(request):
    logout(request)
    messages.info(request, "User was Logged out!")
    return redirect("login")
