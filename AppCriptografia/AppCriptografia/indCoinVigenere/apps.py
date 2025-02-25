from django.apps import AppConfig
import os


class IndcoinvigenereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indCoinVigenere'
    path = os.path.dirname(os.path.abspath(__file__))
