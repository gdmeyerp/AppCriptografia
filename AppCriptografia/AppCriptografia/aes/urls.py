from django.urls import path
from . import views

app_name = 'aes'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.vista_cifrar_aes, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.vista_descifrar_aes, name='descifrar'),  # Vista para descifrar
    path('gallery/', views.gallery, name='gallery'),  # Galeria
]
