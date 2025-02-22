from django.apps import AppConfig
import os
from django.conf import settings


class AnalisisbrauerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AnalisisBrauer'
    path = os.path.join(settings.BASE_DIR, 'AnalisisBrauer')
