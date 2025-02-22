from django.apps import AppConfig
import os
from django.conf import settings


class DesplazamientoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "desplazamiento"
    path = os.path.join(settings.BASE_DIR, 'desplazamiento')
