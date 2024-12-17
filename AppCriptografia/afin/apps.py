from django.apps import AppConfig
import os
from django.conf import settings


class AfinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'afin'
    path = os.path.join(settings.BASE_DIR, 'afin')
