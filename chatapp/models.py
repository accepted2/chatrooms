from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid


class Chatroom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            while Chatroom.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}--{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def get_users(self):
        return User.objects.filter(chatmessage__room=self).distinct()

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
