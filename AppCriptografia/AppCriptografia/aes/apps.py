from django.apps import AppConfig
import os


class AesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aes"
    path = os.path.dirname(os.path.abspath(__file__))
