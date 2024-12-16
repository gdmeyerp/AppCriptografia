from django.apps import AppConfig
import os
from django.conf import settings


class IndicecoincidenciaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indiceCoincidencia'
    path = os.path.join(settings.BASE_DIR, 'indiceCoincidencia')
