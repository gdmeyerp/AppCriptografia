from django.shortcuts import render
from collections import Counter
from .models import HistorialIC

# Frecuencias esperadas de letras en inglés
FRECUENCIAS_INGLES = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 'F': 0.022,
    'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
    'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.001, 'R': 0.060,
    'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
    'Y': 0.020, 'Z': 0.001
}

def calcular_ic(texto):
    """ Calcula el Índice de Coincidencia para un texto """
    texto = ''.join(c for c in texto if c.isalpha()).upper()
    N = len(texto)
    if N <= 1:
        return 0
    frecuencias = Counter(texto)
    return sum(f * (f - 1) for f in frecuencias.values()) / (N * (N - 1))

def similitud_con_ingles(texto):
    """ Calcula la similitud del texto con las frecuencias esperadas en inglés """
    texto = ''.join(c for c in texto if c.isalpha()).upper()
    N = len(texto)
    if N == 0:
        return 0
    frecuencias = Counter(texto)
    similitud = sum((frecuencias.get(letra, 0) / N) * FRECUENCIAS_INGLES[letra] for letra in FRECUENCIAS_INGLES)
    return round(similitud, 5)

def dividir_texto(texto, longitud):
    """
    Divide el texto en bloques intercalados.
    Ejemplo: longitud=3
    Bloque 1: letras en posiciones 0, 3, 6, ...
    Bloque 2: letras en posiciones 1, 4, 7, ...
    Bloque 3: letras en posiciones 2, 5, 8, ...
    """
    bloques = ['' for _ in range(longitud)]
    for i, letra in enumerate(texto):
        bloques[i % longitud] += letra
    return bloques

def analizar_indice_coincidencia(request):
    resultados = []
    texto = ''
    metodo = ''
    longitud_max = 0
    ic_friedman = 0

    if request.method == 'POST':
        texto = request.POST.get('texto', '').upper().replace(' ', '')
        metodo = request.POST.get('metodo', 'Desconocido')
        longitud_max = int(request.POST.get('longitud_max', 0))

        # Índice de Coincidencia global (Friedman)
        ic_friedman = calcular_ic(texto)

        for longitud in range(2, longitud_max + 1):
            bloques = dividir_texto(texto, longitud)
            ic_bloques = []
            similitud_bloques = []

            for bloque in bloques:
                ic = calcular_ic(bloque)
                similitud = similitud_con_ingles(bloque)
                ic_bloques.append(ic)
                similitud_bloques.append(similitud)

            ic_promedio = sum(ic_bloques) / len(ic_bloques)
            similitud_promedio = sum(similitud_bloques) / len(similitud_bloques)

            resultados.append({
                'longitud': longitud,
                'bloques': bloques,  # Mostrar bloques cifrados
                'ic_bloques': [round(ic, 5) for ic in ic_bloques],
                'similitud_bloques': [round(sim, 5) for sim in similitud_bloques],
                'ic_promedio': round(ic_promedio, 5),
                'similitud_promedio': round(similitud_promedio, 5),
            })

            # Guardar en la base de datos
            HistorialIC.objects.create(
                texto=texto,
                metodo=metodo,
                longitud_clave=longitud,
                ic=round(ic_promedio, 5),
                similitud=round(similitud_promedio, 5)
            )

    return render(request, 'indiceCoincidencia/index.html', {
        'resultados': resultados,
        'ic_friedman': round(ic_friedman, 5),
        'texto': texto,
        'metodo': metodo,
        'longitud_max': longitud_max
    })



