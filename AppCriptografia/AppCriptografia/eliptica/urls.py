
from django.urls import path
from .views import index_view, generar_claves_view, cifrar_view, descifrar_view  # Agregar historial si es necesario

app_name = 'eliptica'  # ESTE NOMBRE DEBE COINCIDIR CON EL QUE USAS EN LAS PLANTILLAS

urlpatterns = [
    path('', index_view, name='index'),
    path('generar-claves/', generar_claves_view, name='generar_claves'),
    path('cifrar/', cifrar_view, name='cifrar'),
    path('descifrar/', descifrar_view, name='descifrar'),

]
