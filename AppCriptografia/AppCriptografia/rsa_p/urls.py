from django.urls import path
from . import views

app_name = 'rsa_p'

urlpatterns = [
    path('', views.index, name='index'),
    path('cifrar/', views.cifrar_view, name='cifrar'),
    path('descifrar/', views.descifrar_view, name='descifrar'),
    path('historial/', views.historial_view, name='historial'),
]
