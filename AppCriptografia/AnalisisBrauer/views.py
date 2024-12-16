from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .cifrado import ejecutarAnalisis
from django.contrib import messages
import base64


@login_required
def index(request):
    """Vista principal del módulo Sustitucion"""
    return render(request, 'AnalisisBrauer/index.html')

@login_required
def analisis_view(request):
    """Vista para Analsis de Brauer"""
    sucesiones = None
    dimension_val = None
    dimension_centro_val = None
    img_bytes = None
    imagen_data_uri = None

    if request.method == "POST":
        mensaje = request.POST.get("mensaje", "").strip()
        longitud = request.POST.get("longitud", "").strip()

        if mensaje and longitud:
            try:
                sucesiones, dimension_val, dimension_centro_val, img_bytes = ejecutarAnalisis(mensaje, longitud)
                imagen_base64 = base64.b64encode(img_bytes).decode('utf-8')
                imagen_data_uri = f"data:image/png;base64,{imagen_base64}"
                messages.success(request, "Analisis Ejecutado Satisfactoriamente")
            except Exception as e:
                messages.error(request, f"Error al ejecutar el analisis de Bauer para el mensaje: {e}")
        else :
            messages.error(request, "El mensaje y la longitud son obligatorios.")

    return render(request, "AnalisisBrauer/analisis.html", {
        "dimension_val": dimension_val,
        "dimension_centro_val": dimension_centro_val,
        "sucesiones": sucesiones,
        "image": imagen_data_uri
    })

