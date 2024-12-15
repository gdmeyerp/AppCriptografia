from django.urls import path
from . import views

app_name = 'permutacion'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_permutacion_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_permutacion_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_permutacion_view, name='historial'),  # Historial
]
