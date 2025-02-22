from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MultiplicativoCifrado, MultiplicativoDescifrado
from .cifrado import cifrar_multiplicativo, decifrar_multiplicativo
from django.contrib import messages

@login_required
def index(request):
    """Vista principal del módulo Multiplicativo"""
    return render(request, 'multiplicativo/index.html')

@login_required
def cifrar_view(request):
    """Vista para cifrar un mensaje con Multiplicativo"""
    mensaje_cifrado = None

    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje and clave:
            try:
                mensaje_cifrado = cifrar_multiplicativo(mensaje, clave)
                MultiplicativoCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    clave=clave,
                    mensaje_cifrado=mensaje_cifrado
                )
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")
        else :
            messages.error(request, "El mensaje y la clave son obligatorios.")

    return render(request, "multiplicativo/cifrar.html", {
        "mensaje_cifrado": mensaje_cifrado,
    })

@login_required
def descifrar_view(request):
    """Vista para descifrar un mensaje con Multiplicativo"""
    mensaje_descifrado = None

    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave = request.POST.get("clave", "").strip()

        if mensaje_cifrado and clave:
            try:
                mensaje_descifrado = decifrar_multiplicativo(mensaje_cifrado, clave)
                MultiplicativoDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado=mensaje_cifrado,
                    clave=clave,
                    mensaje_descifrado=mensaje_descifrado
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje y la clave son obligatorios.")

    return render(request, "multiplicativo/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

@login_required
def historial_view(request):
    """Vista para mostrar el historial de cifrado y descifrado con Multiplicativo"""
    cifrados = MultiplicativoCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    descifrados = MultiplicativoDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'multiplicativo/historial.html', {
        'cifrados': cifrados,
        'descifrados': descifrados,
    })

