from typing import List

from pydantic_settings import PydanticSettings


class BaseSettings(PydanticSettings):
    INSTALLED_APPS: List[str] = (
        ["whitenoise.runserver_nostatic"]
        + [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.staticfiles",
        ]
        + ["django_extensions"]
        + []
    )

    MIDDLEWARE: List[str] = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    TEMPLATES: List[dict] = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    STATIC_URL: str = "/static/"

    LOGGING: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }
