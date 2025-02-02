from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Chatroom


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100, label="Username")
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
class CreateRoomForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Room Name")

    class Meta:
        model = Chatroom
        fields = ["name"]
