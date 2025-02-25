from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ElGamalCifrado, ElGamalDescifrado
from .cifrado import elgamal_encrypt, elgamal_decrypt

@login_required
def index(request):
    """Vista principal del módulo ElGamal"""
    return render(request, 'elGamal/index.html')

def dividir_texto(texto, n=50):
    """Divide un número largo en líneas de máximo 'n' caracteres."""
    return "\n".join(texto[i:i+n] for i in range(0, len(texto), n))

@login_required
def cifrar_elGamal_view(request):
    """Vista para cifrar un mensaje con el método ElGamal"""
    mensaje_cifrado1 = None
    mensaje_cifrado2 = None
    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        
        if mensaje:
            try:
                mensaje_cifrado1, mensaje_cifrado2 = elgamal_encrypt(mensaje)
                ElGamalCifrado.objects.create(
                    usuario=request.user,
                    mensaje_original=mensaje,
                    mensaje_cifrado1=mensaje_cifrado1,
                    mensaje_cifrado2=mensaje_cifrado2,
                ) 
                mensaje_cifrado1 = dividir_texto(mensaje_cifrado1)
                mensaje_cifrado2 = dividir_texto(mensaje_cifrado2) 
                messages.success(request, "Mensaje cifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al cifrar el mensaje: {e}")
        else:
            messages.error(request, "El mensaje es obligatorio.")
    return render(request, "elGamal/cifrar.html", {"mensaje_cifrado1": mensaje_cifrado1, "mensaje_cifrado2": mensaje_cifrado2})

@login_required
def descifrar_elGamal_view(request):
    """Vista para descifrar un mensaje con el método elGamal"""
    mensaje_descifrado = None
    if request.method == "POST":
        mensaje_cifrado1 = request.POST.get("mensaje_cifrado_1", "").strip()
        mensaje_cifrado2 = request.POST.get("mensaje_cifrado_2", "").strip()

        if mensaje_cifrado1 and mensaje_cifrado2:
            try:
                mensaje_descifrado = elgamal_decrypt((mensaje_cifrado1, mensaje_cifrado2))
                ElGamalDescifrado.objects.create(
                    usuario=request.user,
                    mensaje_cifrado1=mensaje_cifrado1,
                    mensaje_cifrado2=mensaje_cifrado2,
                    mensaje_descifrado=mensaje_descifrado,
                )
                messages.success(request, "Mensaje descifrado y guardado correctamente.")
            except Exception as e:
                messages.error(request, f"Error al descifrar el mensaje: {e}")
        else:
            messages.error(request, "Los mensajes cifrados son obligatorios.")
    return render(request, "elGamal/descifrar.html", {"mensaje_descifrado": mensaje_descifrado })

@login_required
def historial_elGamal_view(request):
    """Vista para mostrar el historial de cifrados y descifradose con el método El Gamal"""
    tabla = request.GET.get('tabla', 'cifrado')
    datos = ElGamalCifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion') if tabla == 'cifrado' else ElGamalDescifrado.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'elGamal/historial.html', {'datos': datos, 'tabla_seleccionada': tabla})