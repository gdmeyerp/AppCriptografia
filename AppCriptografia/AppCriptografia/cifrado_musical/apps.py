from django.apps import AppConfig
import os


class CifradoMusicalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cifrado_musical'
    path = os.path.dirname(os.path.abspath(__file__))
