from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DesplazamientoCifrado, DesplazamientoDescifrado
from .cifrado import cifrar_desplazamiento, descifrar_desplazamiento

@login_required
def index(request):
    """Vista principal del módulo Desplazamiento"""
    return render(request, 'desplazamiento/index.html')

@login_required
def cifrar_desplazamiento_view(request):
    """Vista para cifrar un mensaje con el método Desplazamiento"""
    mensaje_cifrado = None
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje and clave:
            try:
                mensaje_cifrado = cifrar_desplazamiento(mensaje, clave)
                DesplazamientoCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    clave=clave,
                    mensaje_cifrado=mensaje_cifrado,
                )
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje y la clave son obligatorios.")
    return render(request, "desplazamiento/cifrar.html", {"mensaje_cifrado": mensaje_cifrado})

@login_required
def descifrar_desplazamiento_view(request):
    """Vista para descifrar un mensaje con el método Desplazamiento"""
    mensaje_descifrado = None
    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje_cifrado and clave:
            try:
                mensaje_descifrado = descifrar_desplazamiento(mensaje_cifrado, clave)
                DesplazamientoDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado=mensaje_cifrado,
                    clave=clave,
                    mensaje_descifrado=mensaje_descifrado,
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje cifrado y la clave son obligatorios.")
    return render(request, "desplazamiento/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

@login_required
def historial_desplazamiento_view(request):
    """Vista para mostrar el historial de cifrados y descifradose con el método Desplazamiento"""
    tabla = request.GET.get('tabla', 'cifrado')
    datos = DesplazamientoCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion') if tabla == 'cifrado' else DesplazamientoDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'desplazamiento/historial.html', {'datos': datos, 'tabla_seleccionada': tabla})