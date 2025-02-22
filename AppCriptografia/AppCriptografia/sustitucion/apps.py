from django.apps import AppConfig
import os
from django.conf import settings


class SustitucionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sustitucion'
    path = os.path.join(settings.BASE_DIR, 'sustitucion')
