from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),  # Usa namespace correctamente
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),  # Usa namespace en dashboard
    path('vigenere/', include('vigenere.urls', namespace='vigenere')),  # Usa namespace en vigenere
    path('modulo/rsa/', include('rsa.urls', namespace='rsa')),  # Incluye el módulo RSA
    path('sustitucion/', include('sustitucion.urls', namespace='sustitucion')),  # Usa namespace en sustitucion
    path('multiplicativo/', include('multiplicativo.urls', namespace='multiplicativo')),  # Usa namespace en multiplicativo
    path('hill/', include('hill.urls', namespace='hill')),  # Usa namespace en hill
    path('permutacion/', include('permutacion.urls', namespace='permutacion')),  # Usa namespace en permutacion
    path('indice-coincidencia/', include('indiceCoincidencia.urls')), 

    path('AnalisisBrauer/', include('AnalisisBrauer.urls', namespace='AnalisisBrauer')),  # Usa namespace en permutacion
    path('afin/', include('afin.urls', namespace='afin')),  # Usa namespace en afín
    path('desplazamiento/', include('desplazamiento.urls', namespace='desplazamiento'))  # Usa namespace en desplazamiento
]
