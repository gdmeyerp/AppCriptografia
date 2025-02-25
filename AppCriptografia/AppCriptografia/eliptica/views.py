from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .cifrado import ECCrypto

def index_view(request):
    """ Vista principal del módulo de cifrado. """
    return render(request, 'eliptica/index.html')

def generar_claves_view(request):
    """ Genera claves ECC y las devuelve en JSON. """
    ecc = ECCrypto()
    clave_privada, clave_publica = ecc.generar_claves()

    return JsonResponse({
        'clave_privada': clave_privada.decode(),
        'clave_publica': clave_publica.decode()
    })

def cifrar_view(request):
    """ Cifra un mensaje usando ECC. """
    if request.method == 'POST':
        try:
            print("🔹 Recibiendo solicitud de cifrado...")

            # Capturar datos
            clave_publica_pem = request.POST.get("clave_publica", "").strip()
            mensaje = request.POST.get("mensaje", "").strip()

            print(f"📜 Clave Pública Recibida: {clave_publica_pem[:50]}...")
            print(f"📄 Mensaje a Cifrar: {mensaje[:50]}...")

            # Verificar si los datos están vacíos
            if not clave_publica_pem or not mensaje:
                print("❌ ERROR: Faltan datos en la solicitud.")
                return JsonResponse({"error": "Faltan datos en la solicitud."}, status=400)

            # Instanciar cifrado
            ecc = ECCrypto()
            clave_efimera_pem, iv, etiqueta, mensaje_cifrado = ecc.cifrar(clave_publica_pem, mensaje)

            print("✅ Cifrado exitoso.")
            return JsonResponse({
                "clave_efimera_pem": clave_efimera_pem,
                "iv": iv,
                "etiqueta": etiqueta,
                "mensaje_cifrado": mensaje_cifrado
            })

        except Exception as e:
            print(f"⚠️ ERROR en cifrado: {str(e)}")
            return JsonResponse({"error": f"Error en el cifrado: {str(e)}"}, status=400)

    return render(request, "eliptica/cifrar.html")

def descifrar_view(request):
    """ Descifra un mensaje usando ECC. """
    if request.method == 'POST':
        try:
            print("🔹 Recibiendo solicitud de descifrado...")

            # Capturar datos
            clave_privada_pem = request.POST.get("clave_privada", "").strip()
            clave_efimera_pem = request.POST.get("clave_efimera", "").strip()
            iv = request.POST.get("iv", "").strip()
            etiqueta = request.POST.get("etiqueta", "").strip()
            mensaje_cifrado = request.POST.get("mensaje_cifrado", "").strip()

            # Verificar si hay datos vacíos
            if not clave_privada_pem or not clave_efimera_pem or not iv or not etiqueta or not mensaje_cifrado:
                print("❌ ERROR: Faltan datos en la solicitud.")
                return JsonResponse({"error": "Faltan datos en la solicitud."}, status=400)

            # Instanciar cifrado
            ecc = ECCrypto()
            mensaje_descifrado = ecc.descifrar(clave_privada_pem, clave_efimera_pem, iv, etiqueta, mensaje_cifrado)

            print("✅ Descifrado exitoso.")
            return JsonResponse({"mensaje_descifrado": mensaje_descifrado})

        except Exception as e:
            print(f"⚠️ ERROR en descifrado: {str(e)}")
            return JsonResponse({"error": f"Error en el descifrado: {str(e)}"}, status=400)

    return render(request, "eliptica/descifrar.html")
