from django.urls import path
from . import views

app_name = 'elGamal'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_elGamal_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_elGamal_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_elGamal_view, name='historial'),  # Historial
]
