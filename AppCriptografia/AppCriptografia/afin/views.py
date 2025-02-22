from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AfinCifrado, AfinDescifrado
from .cifrado import cifrar_afin, descifrar_afin

@login_required
def index(request):
    return render(request, 'afin/index.html')

@login_required
def cifrar_afin_view(request):
    """Vista para cifrar un mensaje con el método Afin"""
    mensaje_cifrado = None
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        clave_a = request.POST.get("clave_a", "").strip()
        clave_b = request.POST.get("clave_b", "").strip()

        if mensaje and clave_a and clave_b:
            try:
                clave_a = int(clave_a)
                clave_b = int(clave_b)
                mensaje_cifrado = cifrar_afin(mensaje, clave_a, clave_b)
                AfinCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    clave_a=clave_a,
                    clave_b=clave_b,
                    mensaje_cifrado=mensaje_cifrado,
                )
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje, la clave 'a' y la clave 'b' son obligatorios.")
    return render(request, "afin/cifrar.html", {"mensaje_cifrado": mensaje_cifrado})

@login_required
def descifrar_afin_view(request):
    """Vista para descifrar un mensaje con el método Afin"""
    mensaje_descifrado = None
    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave_a = request.POST.get("clave_a", "").strip()
        clave_b = request.POST.get("clave_b", "").strip()

        if mensaje_cifrado and clave_a and clave_b:
            try:
                clave_a = int(clave_a)
                clave_b = int(clave_b)
                mensaje_descifrado = descifrar_afin(mensaje_cifrado, clave_a, clave_b)
                AfinDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado=mensaje_cifrado,
                    clave_a=clave_a,
                    clave_b=clave_b,
                    mensaje_descifrado=mensaje_descifrado,
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje cifrado, la clave 'a' y la clave 'b' son obligatorios.")
    return render(request, "afin/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

@login_required
def historial_afin_view(request):
    """Vista para mostrar el historial de cifrados y descifrados con el método Afin"""
    tabla = request.GET.get('tabla', 'cifrado')
    datos = AfinCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion') if tabla == 'cifrado' else AfinDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'afin/historial.html', {'datos': datos, 'tabla_seleccionada': tabla})
