from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from core.models import HistorialCifrado

from vigenere.models import VigenereCifrado, VigenereDescifrado
from sustitucion.models import SustitucionCifrado, SustitucionDescifrado

from multiplicativo.models import MultiplicativoCifrado, MultiplicativoDescifrado

from hill.models import HillCifrado, HillDescifrado
from permutacion.models import PermutacionCifrado, PermutacionDescifrado

from afin.models import AfinCifrado, AfinDescifrado
from desplazamiento.models import DesplazamientoCifrado, DesplazamientoDescifrado
from cifrado_musical.models import PartituraCifrada, PartituraDescifrada


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
    elif tabla == 'sustitucion_cifrado':
        datos = SustitucionCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'sustitucion_descifrado':
        datos = SustitucionDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'multiplicativo_cifrado':
        datos = MultiplicativoCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'multiplicativo_descifrado':
        datos = MultiplicativoDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'hill_cifrado':
        datos = HillCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'hill_descifrado':
        datos = HillDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'permutacion_cifrado':
        datos = PermutacionCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'permutacion_descifrado':
        datos = PermutacionDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'afin_cifrado':
        datos = AfinCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'afin_descifrado':
        datos = AfinDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'desplazamiento_cifrado':
        datos = DesplazamientoCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'desplazamiento_descifrado':
        datos = DesplazamientoDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'cifrado_musical_cifrado':
        datos = PartituraCifrada.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    elif tabla == 'cifrado_musical_descifrado':
        datos = PartituraDescifrada.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    else:
        datos = []

    return render(request, 'dashboard/historial_dinamico.html', {
        'datos': datos,
        'tabla_seleccionada': tabla,
    })


@login_required
def cargar_modulo(request, modulo):
    """Carga dinámicamente los módulos dentro del dashboard"""
    modulos_disponibles = ['vigenere', 'rsa', 'cesar','cifrado_musical', 'sustitucion', 'multiplicativo','hill','permutacion', 'afin', 'desplazamiento']  # Lista de módulos admitidos
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
        #{'nombre': 'César', 'slug': 'cesar', 'imagen': 'cesar.jpg', 'descripcion': 'Desplaza las letras un número fijo.'},
        {'nombre': 'RSA', 'slug': 'rsa', 'imagen': 'rsa.jpg', 'descripcion': 'Cifrado asimétrico basado en claves pública y privada.'},
        {'nombre': 'Multiplicativo', 'slug': 'multiplicativo', 'imagen': None, 'descripcion': 'Cifra mensajes multiplicando por una clave.'},
        {'nombre': 'Sustitucion', 'slug': 'sustitucion', 'imagen': None, 'descripcion': 'Cifra mensajes sustituyendo cada elemento de acuerdo a una permutacion.'},
        {'nombre': 'Hill', 'slug': 'hill', 'imagen': None, 'descripcion': 'Cifrado basado en transformaciones lineales.'},
        {'nombre': 'Permutación', 'slug': 'permutacion', 'imagen': None, 'descripcion': 'Cifrado basado en matrices de permutación.'},
        {'nombre': 'Afín', 'slug': 'afin', 'imagen': None, 'descripcion': 'Cifrado basado en combinaciones lineales de letras.'},
        {'nombre': 'Desplazamiento', 'slug': 'desplazamiento', 'imagen': None, 'descripcion': 'Cifra mensajes desplazando las letras por un número fijo.'},
        {'nombre': 'Cifrado Musical', 'slug': 'cifrado_musical', 'imagen': 'musical.jpg', 'descripcion': 'Cifra partituras musicales alterando sus notas.'},

    ]

    # Asignar una imagen y descripción por defecto si no están definidas
    for metodo in metodos:
        if 'imagen' not in metodo or not metodo['imagen']:
            metodo['imagen'] = 'default.jpg'  # Imagen por defecto
        if 'descripcion' not in metodo or not metodo['descripcion']:
            metodo['descripcion'] = 'Sin descripción disponible.'  # Descripción por defecto

    return render(request, 'dashboard/cifrar_metodos.html', {'metodos': metodos})
