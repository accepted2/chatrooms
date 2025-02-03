from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, logoutUser

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("rooms/<int:room_id>/", views.chatroom, name="chatroom"),
]
