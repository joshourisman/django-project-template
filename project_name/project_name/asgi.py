from django.core.asgi import get_asgi_application
from pydantic_settings import SetUp

SetUp().configure()

application = get_asgi_application()
