from configurations import values

from .base import Base


class LocalDev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = True
    DATABASES = values.DatabaseURLValue("postgres://localhost/{{ project_name }}")

    INTERNAL_IPS = ["127.0.0.1"]

    SECRET_KEY = values.Value("!!!!INSECURE SECRET KEY!!!!")
