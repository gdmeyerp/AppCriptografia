from django.urls import path
from . import views

app_name = 'hill'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_hill_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_hill_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_hill_view, name='historial'),  # Historial
]
