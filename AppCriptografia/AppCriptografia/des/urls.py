from django.urls import path
from . import views

app_name = 'des'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('cifrar/', views.vista_cifrar_des, name='cifrar'),  # Vista para cifrar
    path('descifrar/', views.vista_descifrar_des, name='descifrar'),  # Vista para descifrar
    path('gallery/', views.gallery, name='gallery'),  # Galeria
]
