from django.urls import path
from . import views

app_name = 'multiplicativo'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_view, name='historial'),  # Historial
]
