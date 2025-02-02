from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="chatapp/login.html"),
        name="login",
    ),
    path("logout/", views.logoutUser, name="logout"),
    path("rooms/<slug:slug>/<int:room_id>/", views.chatroom, name="chatroom"),
]
