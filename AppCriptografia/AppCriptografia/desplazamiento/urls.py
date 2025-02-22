from django.urls import path
from . import views

app_name = 'desplazamiento'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_desplazamiento_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_desplazamiento_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_desplazamiento_view, name='historial'),  # Historial
]
