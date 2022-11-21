import os


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,  URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
django_asgi_app = get_asgi_application()

from snippets import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket" : URLRouter(routing.websocket_urlpatterns),
    }
)