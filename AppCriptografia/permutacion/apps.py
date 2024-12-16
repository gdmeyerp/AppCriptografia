from django.apps import AppConfig
import os
from django.conf import settings


class PermutacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "permutacion"
    path = os.path.join(settings.BASE_DIR, 'permutacion')
