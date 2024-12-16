from django.apps import AppConfig
import os
from django.conf import settings


class HillConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hill"
    path = os.path.join(settings.BASE_DIR, 'hill')
