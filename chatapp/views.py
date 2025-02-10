from django.shortcuts import get_object_or_404, redirect, render
from .models import Chatroom, ChatMessage
from .forms import RegisterForm, CreateRoomForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("register")
    if request.method == "POST":
        print(request.POST)
        form = CreateRoomForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, "Chatroom created!")
            return redirect("index")
        else:
            messages.error(
                request, "Error creating chatroom. Room with this name already exists."
            )

    form = CreateRoomForm()
    chatrooms = Chatroom.objects.all()
    print(chatrooms)
    return render(
        request,
        "chatapp/index.html",
        {"chatrooms": chatrooms, "form": form},
    )


@login_required(login_url="login")
def chatroom(request, room_id):
    # chatroom = Chatroom.objects.get(slug=slug)
    chatrooms = Chatroom.objects.all()
    chatroom = get_object_or_404(Chatroom, id=room_id)
    chat_messages = ChatMessage.objects.filter(room=chatroom)
    users = chatroom.get_users()

    return render(
        request,
        "chatapp/room.html",
        {
            "chatroom": chatroom,
            "chat_messages": chat_messages,
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
            return redirect("index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")
    else:
        form = RegisterForm()

    return render(request, "chatapp/register.html", {"form": form})


# Для логина используем стандартное представление
class CustomLoginView(LoginView):
    template_name = "chatapp/login.html"
    print("error")

    def form_valid(self, form):
        messages.success(self.request, "You are logged in!")
        return super().form_valid(form)

    def form_invalid(self, form):

        errors = form.errors.get("__all__")

        if errors:
            for error in errors:
                messages.error(self.request, error)
                print(error)
        return self.render_to_response(self.get_context_data(form=form))


def logoutUser(request):
    logout(request)
    messages.info(request, "User was Logged out!")
    return redirect("login")


def delete_room(request, id):
    room = Chatroom.objects.get(id=id)
    if request.user == room.owner:
        if request.method == "POST":
            room.delete()
            return redirect("index")
