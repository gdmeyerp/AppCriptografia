from django.urls import path
from . import views

app_name = 'afin'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.cifrar_afin_view, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.descifrar_afin_view, name='descifrar'),  # Vista para descifrar
    path('historial/', views.historial_afin_view, name='historial'),  # Historial
]
