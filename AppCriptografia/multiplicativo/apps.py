from django.apps import AppConfig
import os
from django.conf import settings


class MultiplicativoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multiplicativo'
    path = os.path.join(settings.BASE_DIR, 'multiplicativo')
