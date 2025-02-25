from django.apps import AppConfig
import os


class RsaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rsa'
    path = os.path.dirname(os.path.abspath(__file__))
