from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RsaCifrado, RsaDescifrado
from .cifrado import generar_claves, cifrar_rsa, descifrar_rsa
from django.contrib import messages

@login_required
def index(request):
    """Vista principal del módulo RSA"""
    return render(request, 'rsa/index.html')

@login_required
def cifrar_view(request):
    """Vista para cifrar un mensaje con RSA"""
    mensaje_cifrado = None
    clave_publica, clave_privada = generar_claves()

    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()

        if mensaje:
            try:
                mensaje_cifrado = cifrar_rsa(mensaje, clave_publica)
                RsaCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    clave_publica=clave_publica,
                    mensaje_cifrado=mensaje_cifrado
                )
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")

    return render(request, "rsa/cifrar.html", {
        "mensaje_cifrado": mensaje_cifrado,
        "clave_publica": clave_publica,
        "clave_privada": clave_privada,
    })

@login_required
def descifrar_view(request):
    """Vista para descifrar un mensaje con RSA"""
    mensaje_descifrado = None

    if request.method == "POST":
        mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()
        clave_privada = request.POST.get("clave_privada", "").strip()

        if mensaje_cifrado and clave_privada:
            try:
                mensaje_descifrado = descifrar_rsa(mensaje_cifrado, clave_privada)
                RsaDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado=mensaje_cifrado,
                    clave_privada=clave_privada,
                    mensaje_descifrado=mensaje_descifrado
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")

    return render(request, "rsa/descifrar.html", {"mensaje_descifrado": mensaje_descifrado})

@login_required
def historial_view(request):
    """Vista para mostrar el historial de cifrado y descifrado con RSA"""
    cifrados = RsaCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    descifrados = RsaDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'rsa/historial.html', {
        'cifrados': cifrados,
        'descifrados': descifrados,
    })
