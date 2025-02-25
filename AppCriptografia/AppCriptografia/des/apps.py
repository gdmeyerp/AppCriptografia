from django.apps import AppConfig
import os


class DesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "des"
    path = os.path.dirname(os.path.abspath(__file__))
