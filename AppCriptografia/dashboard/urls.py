from . import views
from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),  # Página principal del dashboard
    path('cifrar/', views.cifrar_metodos, name='cifrar_metodos'),  # Lista de métodos
    path('modulo/<str:modulo>/', views.cargar_modulo, name='cargar_modulo'),  # Cargar un módulo dinámico
    path('modulo/vigenere/', include('vigenere.urls', namespace='vigenere')),  # Incluye las rutas del módulo Vigenère
    path('historial/', views.historial_dinamico, name='historial_dinamico'),  # Nueva vista dinámica
    path('modulo/rsa/', include('rsa.urls', namespace='rsa')),  # Incluye el módulo RSA
    path('modulo/sustitucion/', include('sustitucion.urls', namespace='sustitucion')),  # Incluye las rutas del módulo Sustitucion

]
