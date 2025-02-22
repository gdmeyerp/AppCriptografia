from django.urls import path
from . import views

app_name = 'AnalisisBrauer'

urlpatterns = [
    path('', views.index, name='index'),  # Página principal del módulo
    path('analisis/', views.analisis_view, name='analisis'),  # Vista para el analisis
]
