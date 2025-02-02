import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatapp.routing  # Убедись, что этот импорт правильный

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Инициализируем Django ASGI-приложение
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Используем уже созданное приложение
        "websocket": AuthMiddlewareStack(
            URLRouter(chatapp.routing.websocket_urlpatterns)
        ),
    }
)
