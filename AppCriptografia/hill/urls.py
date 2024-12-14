from django.urls import path
from . import views

app_name = 'vigenere'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_vigenere_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_vigenere_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_vigenere_view, name='historial'),  # Historial
]
