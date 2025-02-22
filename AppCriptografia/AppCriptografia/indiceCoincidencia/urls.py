from django.urls import path
from . import views

app_name = 'indiceCoincidencia'

urlpatterns = [
    path('', views.analizar_indice_coincidencia, name='indice_coincidencia'),
    path('guardar/', views.analizar_indice_coincidencia, name='guardar'),  # Ajustar esta vista si es necesario
]
