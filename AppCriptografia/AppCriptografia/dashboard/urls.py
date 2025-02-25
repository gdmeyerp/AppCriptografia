from . import views
from django.urls import path, include

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),  # Página principal del dashboard
    path('cifrar/', views.cifrar_metodos, name='cifrar_metodos'),  # Lista de métodos
    path('modulo/<str:modulo>/', views.cargar_modulo, name='cargar_modulo'),  # Cargar un módulo dinámico
    path('modulo/vigenere/', include('vigenere.urls', namespace='vigenere')),  # Incluye las rutas del módulo Vigenère
    path('historial/', views.historial_dinamico, name='historial_dinamico'),  # Nueva vista dinámica
    path('modulo/rsa_p/', include('rsa_p.urls', namespace='rsa')),  # Incluye el módulo RSA
    path('modulo/sustitucion/', include('sustitucion.urls', namespace='sustitucion')),  # Incluye las rutas del módulo Sustitucion
    path('modulo/multiplicativo/', include('multiplicativo.urls', namespace='multiplicativo')),  # Incluye las rutas del módulo Multiplicativo
    path('modulo/hill/', include('hill.urls', namespace='hill')),  # Incluye las rutas del módulo Hill
    path('modulo/permutacion/', include('permutacion.urls', namespace='permutacion')),  # Incluye las rutas del módulo Permutación
    path('modulo/AnalisisBrauer/', include('AnalisisBrauer.urls', namespace='AnalisisBrauer')),  # Incluye las rutas del módulo AnalisisBrauer
    path('modulo/afin/', include('afin.urls', namespace='afin')),  # Incluye las rutas del módulo Afín
    path('modulo/desplazamiento/', include('desplazamiento.urls', namespace='desplazamiento')), # Incluye las rutas del módulo Desplazamiento
    path('modulo/cifrado_musical/', include('cifrado_musical.urls', namespace='cifrado_musical')),
    path('modulo/firmaDocumentos/', include('firmaDocumentos.urls', namespace='firmaDocumentos')),
    path('modulo/elGamal/', include('elGamal.urls', namespace='elGamal')),
    path('modulo/des/', include('des.urls', namespace='des')), # Incluye las rutas del módulo DES
    path('modulo/aes/', include('aes.urls', namespace='aes')) # Incluye las rutas del módulo AES

]
