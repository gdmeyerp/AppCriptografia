from django.contrib import admin
from .models import PartituraCifrada, PartituraDescifrada

# Registrar los modelos en Django Admin
@admin.register(PartituraCifrada)
class PartituraCifradaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'archivo_original', 'archivo_cifrado', 'clave', 'fecha_creacion')
    search_fields = ('usuario__username', 'archivo_original')
    list_filter = ('fecha_creacion', 'clave')

@admin.register(PartituraDescifrada)
class PartituraDescifradaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'archivo_cifrado', 'archivo_descifrado', 'clave', 'fecha_creacion')
    search_fields = ('usuario__username', 'archivo_cifrado')
    list_filter = ('fecha_creacion', 'clave')
