import os


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,  URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import snippets.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": 
            AuthMiddlewareStack(URLRouter(snippets.routing.websocket_urlpatterns)),
    
    }
)
