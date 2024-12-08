from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),  # Usa namespace correctamente
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),  # Usa namespace en dashboard
    path('vigenere/', include('vigenere.urls', namespace='vigenere')),  # Usa namespace en vigenere
    path('modulo/rsa/', include('rsa.urls', namespace='rsa')),  # Incluye el módulo RSA

]