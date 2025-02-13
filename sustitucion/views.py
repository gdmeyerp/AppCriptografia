from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SustitucionCifrado, SustitucionDescifrado
from .cifrado import cifrar_sustitucion, decifrar_sustitucion
from django.contrib import messages

@login_required
def index(request):
    """Vista principal del módulo Sustitucion"""
    return render(request, 'sustitucion/index.html')

@login_required
def cifrar_view(request):
    """Vista para cifrar un mensaje con Sustitucion"""
    mensaje_cifrado = None

    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        permutacion = request.POST.get("permutacion", "").strip()

        if mensaje and permutacion:
            try:
                mensaje_cifrado = cifrar_sustitucion(mensaje, permutacion)
                SustitucionCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    permutacion=permutacion,
                    mensaje_cifrado=mensaje_cifrado
                )
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")
        else :
            messages.error(request, "El mensaje y la permutacion son obligatorios.")

    return render(request, "sustitucion/cifrar.html", {
        "mensaje_cifrado": mensaje_cifrado,
    })

@login_required
def descifrar_view(request):
    """Vista para descifrar un mensaje con Sustitucion"""
    mensaje_descifrado = None

    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        permutacion = request.POST.get("permutacion", "").strip()

        if mensaje_cifrado and permutacion:
            try:
                mensaje_descifrado = decifrar_sustitucion(mensaje_cifrado, permutacion)
                SustitucionDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado=mensaje_cifrado,
                    permutacion=permutacion,
                    mensaje_descifrado=mensaje_descifrado
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje y la permutacion son obligatorios.")

    return render(request, "sustitucion/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

@login_required
def historial_view(request):
    """Vista para mostrar el historial de cifrado y descifrado con Sustitucion"""
    cifrados = SustitucionCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    descifrados = SustitucionDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'sustitucion/historial.html', {
        'cifrados': cifrados,
        'descifrados': descifrados,
    })

