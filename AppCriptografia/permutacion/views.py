from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VigenereCifrado, VigenereDescifrado
from .cifrado import cifrar_vigenere, descifrar_vigenere

# Vista principal del módulo de Cifrado de Permutación
@login_required
def index(request):
    return render(request, 'permutacion/index.html')

# Vista para cifrar un mensaje con el método de Cifrado de Permutación
@login_required
def cifrar_permutacion_view(request):
    mensaje_cifrado = None
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje and clave:
            try:
                mensaje_cifrado = cifrar_permutacion(mensaje, clave)
                PermutacionCifrado.objects.create(
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
    return render(request, "vigenere/cifrar.html", {"mensaje_cifrado": mensaje_cifrado})

# Vista para descifrar un mensaje con el método Vigenère
@login_required
def descifrar_permutacion_view(request):
    mensaje_descifrado = None
    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje_cifrado and clave:
            try:
                mensaje_descifrado = descifrar_vigenere(mensaje_cifrado, clave)
                PermutacionDescifrado.objects.create(
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
    return render(request, "permutacion/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

# Vista para mostrar el historial de cifrados y descifrados
@login_required
def historial_permutacion_view(request):
    tabla = request.GET.get('tabla', 'cifrado')
    datos = PermutacionCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion') if tabla == 'cifrado' else PermutacionDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'permutacion/historial.html', {'datos': datos, 'tabla_seleccionada': tabla})
