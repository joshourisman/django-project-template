"""
Django settings for {{ project_name }} project.

This project uses django-configurations to manage settings, for more
information on django-configurations, see
http://django-configurations.readthedocs.org/en/latest/

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

import os

from configurations import Configuration, values


class BaseConfiguration(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    SECRET_KEY = '!!!!INSECURE SECRET KEY!!!!'
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = []
    ROOT_URLCONF = '{{ project_name }}.urls'
    WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/New_York'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    STATIC_URL = '/static/'
    DATABASES = values.DatabaseURLValue()


class Develop(BaseConfiguration):
    DEBUG = True
    TEMPLATE_DEBUG = False


class Production(BaseConfiguration):
    SECRET_KEY = '{{ secret_key }}'
