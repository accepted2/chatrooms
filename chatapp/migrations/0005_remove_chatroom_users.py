# Generated by Django 5.1.2 on 2025-01-30 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_chatroom_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='users',
        ),
    ]
