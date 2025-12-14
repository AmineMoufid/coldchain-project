import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import DHT.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(DHT.routing.websocket_urlpatterns)
    ),
})
