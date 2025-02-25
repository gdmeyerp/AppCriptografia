from django.apps import AppConfig
import os


class ElgamalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elGamal'
    path = os.path.dirname(os.path.abspath(__file__))
