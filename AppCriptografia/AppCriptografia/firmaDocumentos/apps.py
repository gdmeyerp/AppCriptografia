from django.apps import AppConfig
import os

class FirmadocumentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firmaDocumentos'
    path = os.path.dirname(os.path.abspath(__file__))
