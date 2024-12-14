from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HillCifrado, HillDescifrado
from .cifrado import cifrar_hill, descifrar_hill

# Vista principal del módulo Hill
@login_required
def index(request):
    return render(request, 'hill/index.html')

# Vista para cifrar un mensaje con el método Hill
@login_required
def cifrar_hill_view(request):
    mensaje_cifrado = None
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje and clave:
            try:
                mensaje_cifrado = cifrar_hill(mensaje, clave)
                HillCifrado.objects.create(
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
    return render(request, "hill/cifrar.html", {"mensaje_cifrado": mensaje_cifrado})

# Vista para descifrar un mensaje con el método Hill
@login_required
def descifrar_hill_view(request):
    mensaje_descifrado = None
    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje_cifrado and clave:
            try:
                mensaje_descifrado = descifrar_hill(mensaje_cifrado, clave)
                HillDescifrado.objects.create(
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
    return render(request, "hill/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

# Vista para mostrar el historial de cifrados y descifrados
@login_required
def historial_hill_view(request):
    tabla = request.GET.get('tabla', 'cifrado')
    datos = HillCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion') if tabla == 'cifrado' else HillDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'hill/historial.html', {'datos': datos, 'tabla_seleccionada': tabla})