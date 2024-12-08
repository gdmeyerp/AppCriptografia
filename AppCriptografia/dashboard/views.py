from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import HistorialCifrado

from vigenere.models import VigenereCifrado, VigenereDescifrado

@login_required
def historial_dinamico(request):
    """Vista para mostrar las tablas dinámicas según el método y tipo de acción"""
    tabla = request.GET.get('tabla', 'vigenere_cifrado')  # Tabla seleccionada, por defecto Vigenere Cifrado

    # Datos inicializados como vacíos
    datos = []

    # Lógica para seleccionar qué tabla cargar
    if tabla == 'vigenere_cifrado':
        datos = VigenereCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'vigenere_descifrado':
        datos = VigenereDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    else:
        datos = []

    return render(request, 'dashboard/historial_dinamico.html', {
        'datos': datos,
        'tabla_seleccionada': tabla,
    })


@login_required
def cargar_modulo(request, modulo):
    """Carga dinámicamente los módulos dentro del dashboard"""
    modulos_disponibles = ['vigenere', 'rsa', 'cesar','11']  # Lista de módulos admitidos
    if modulo in modulos_disponibles:
        return redirect(f'{modulo}:index')  # Redirige dinámicamente al índice del módulo
    else:
        return render(request, 'dashboard/404.html', {'modulo': modulo})


@login_required
def index_view(request):
    """Vista principal del dashboard que muestra los módulos disponibles"""
    modulos = [
        {'nombre': 'Cifrar Mensaje', 'slug': 'dashboard:cifrar_metodos'},  # Ruta actualizada
        {'nombre': 'Historial', 'slug': 'core:historial'},  # Ruta actualizada
    ]
    return render(request, 'dashboard/index.html', {'modulos': modulos})



@login_required
def cifrar_metodos(request):
    """Vista para mostrar los métodos de cifrado disponibles."""
    metodos = [
        {'nombre': 'Vigenère', 'slug': 'vigenere', 'imagen': 'vigenere.jpg', 'descripcion': 'Método clásico basado en una clave repetitiva.'},
        {'nombre': 'César', 'slug': 'cesar', 'imagen': 'cesar.jpg', 'descripcion': 'Desplaza las letras un número fijo.'},
        {'nombre': 'RSA', 'slug': 'rsa', 'imagen': 'rsa.jpg', 'descripcion': 'Cifrado asimétrico basado en claves pública y privada.'},
        {'nombre': 'Afin', 'slug': 'afin', 'descripcion': 'Método que usa funciones afines.'},
        {'nombre': 'Multiplicativo', 'slug': 'multiplicativo', 'imagen': None, 'descripcion': 'Cifra mensajes multiplicando por una clave.'},
    ]

    # Asignar una imagen y descripción por defecto si no están definidas
    for metodo in metodos:
        if 'imagen' not in metodo or not metodo['imagen']:
            metodo['imagen'] = 'default.jpg'  # Imagen por defecto
        if 'descripcion' not in metodo or not metodo['descripcion']:
            metodo['descripcion'] = 'Sin descripción disponible.'  # Descripción por defecto

    return render(request, 'dashboard/cifrar_metodos.html', {'metodos': metodos})
