from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_groupe_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_groupe_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_groupe_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room = data["room"]

        room_exists = await self.save_message(username, room, message)

        if not room_exists:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "Этот чат был удален.",
                        "username": "System",
                        "room": room,
                    }
                )
            )
            # Ожидаем от клиента закрытие подключения или перенаправление
            await self.close()

        else:
            await self.channel_layer.group_send(
                self.room_groupe_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "room": room,
                },
            )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "room": room,
                }
            )
        )

    @sync_to_async
    def save_message(self, username, room, message):
        from django.contrib.auth.models import User  # Перемещено сюда
        from .models import Chatroom, ChatMessage  # Добавлен импорт ChatMessage
        from django.core.exceptions import ObjectDoesNotExist

        try:
            user = User.objects.get(username=username)
            room = Chatroom.objects.get(slug=room)
            ChatMessage.objects.create(user=user, room=room, message=message)
            return True
        except ObjectDoesNotExist:
            print(f"комната {room} больше не существует")
            return False
