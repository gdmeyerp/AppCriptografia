from django.urls import path
from . import views
from .views import encriptar_midi

app_name = 'cifrado_musical'

urlpatterns = [
    path('', views.index, name='index'),
    path('cifrar/', views.cifrar_partitura_view, name='cifrar'),
    path("encriptar_midi/", encriptar_midi, name="encriptar_midi"),

    path('descifrar/', views.descifrar_partitura_view, name='descifrar'),
    path('historial/', views.historial_partituras_view, name='historial'),
]
