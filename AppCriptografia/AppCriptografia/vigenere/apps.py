from django.apps import AppConfig
import os


class VigenereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vigenere'
    path = os.path.dirname(os.path.abspath(__file__))
