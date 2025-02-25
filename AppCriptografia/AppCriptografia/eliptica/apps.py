from django.apps import AppConfig
import os


class ElipticaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eliptica'
    path = os.path.dirname(os.path.abspath(__file__))
