from django.contrib import admin
from .models import Chatroom, ChatMessage

# Register your models here.


class ChatroomAdmin(admin.ModelAdmin):
    list_display = ["name", "get_users_list"]

    def get_users_list(self, obj):
        return ",".join(user.username for user in obj.get_users())

    get_users_list.short_description = "Пользователи"


admin.site.register(Chatroom, ChatroomAdmin)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["user", "room_name", "message", "date"]
    list_filter = ["room", "date"]
    search_fields = ["user", "room", "message"]

    def room_name(self, obj):
        return obj.room.name

    room_name.short_description = "Room Name"


admin.site.register(ChatMessage, ChatMessageAdmin)
