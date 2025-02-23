from django.urls import path 
from .views import upload_file_sign, validate_sign_view, index, historial_firmas_view

app_name = "firmaDocumentos"

urlpatterns = [ 
    path('', index, name='index'),
    path('cifrar/', upload_file_sign, name= 'cifrar'), 
    path('validar/', validate_sign_view, name= 'validar'), 
    path('historial/', historial_firmas_view, name='historial'),
]