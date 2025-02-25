from django.apps import AppConfig
import os


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    path = os.path.dirname(os.path.abspath(__file__))
