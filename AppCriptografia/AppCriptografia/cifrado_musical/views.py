from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from .models import PartituraCifrada, PartituraDescifrada
from .cifrado import cifrar_partitura, descifrar_partitura
import os
import mido


def noteToMidi(note_name):
    """
    Convierte un nombre de nota (ejemplo: 'C#5') en un número MIDI (0-127).
    """
    import re
    # Array de notas (C => semitone 0, C# => 1, etc.)
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    match = re.match(r'^([A-G][#b]?)(\d+)$', note_name)
    if not match:
        return None
    note_part, octave_str = match.groups()
    if note_part not in notes:
        return None
    semitone = notes.index(note_part)
    octave = int(octave_str)
    # MIDI: C0 = 12 => (octave + 1)*12 + semitone
    return semitone + (octave + 1)*12

@csrf_exempt
def crear_midi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            encrypted_notes = data.get('encryptedNotes', [])
            tempo = data.get('tempo', 120)

            mid = mido.MidiFile()
            track = mido.MidiTrack()
            mid.tracks.append(track)

            # Tempo
            tempo_msg = mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo))
            track.append(tempo_msg)

            # Duración fija
            duration_ticks = 480
            for note in encrypted_notes:
                note_number = noteToMidi(note)  # Define noteToMidi en el mismo archivo o impórtalo
                if note_number is None:
                    continue
                on = mido.Message('note_on', note=note_number, velocity=64, time=0)
                off = mido.Message('note_off', note=note_number, velocity=64, time=duration_ticks)
                track.append(on)
                track.append(off)

            # Guardar en MEDIA_ROOT
            midi_filename = 'midi_encriptado.mid'
            midi_path = os.path.join(settings.MEDIA_ROOT, midi_filename)
            os.makedirs(os.path.dirname(midi_path), exist_ok=True)
            mid.save(midi_path)

            download_url = settings.MEDIA_URL + midi_filename
            return JsonResponse({'url': download_url})
        except Exception as e:
            print("Error en crear_midi:", e)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def encriptar_midi(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            metodo = data.get("metodo")
            parametros = {k: v for k, v in data.items() if k != "metodo"}
            input_path = os.path.join(settings.MEDIA_ROOT, "midi_original.mid")
            output_path = os.path.join(settings.MEDIA_ROOT, "midi_encriptado.mid")
            cifrar_partitura(input_path, output_path, metodo=metodo, **parametros)
            return JsonResponse({
                "success": True,
                "message": "Encriptación exitosa",
                "file_url": f"/media/midi_encriptado.mid"
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)



@login_required
def cifrar_partitura_view(request):
    archivo_cifrado_url = None  # URL accesible para la plantilla

    if request.method == "POST" and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        clave = int(request.POST.get("clave", 3))

        partitura = PartituraCifrada.objects.create(
            usuario=request.user,
            archivo_original=archivo,
            clave=clave,
        )

        # Rutas de entrada y salida
        input_path = os.path.join(settings.MEDIA_ROOT, partitura.archivo_original.name)
        output_dir = os.path.join(settings.MEDIA_ROOT, 'partituras/cifradas/')
        os.makedirs(output_dir, exist_ok=True)  # Asegurar que la carpeta exista

        output_filename = partitura.archivo_original.name.replace('.mid', '_cifrado.mid')
        output_path = os.path.join(output_dir, output_filename)

        try:
            cifrar_partitura(input_path, output_path, clave)

            # Guardar la ruta correcta en la base de datos
            partitura.archivo_cifrado.name = f'partituras/cifradas/{output_filename}'
            partitura.save()

            # Construir URL accesible
            archivo_cifrado_url = f"{settings.MEDIA_URL}{partitura.archivo_cifrado}"
            messages.success(request, "✅ Partitura cifrada correctamente.")

        except Exception as e:
            messages.error(request, f"❌ Error al cifrar la partitura: {e}")

    return render(request, "cifrado_musical/cifrar.html", {
        "archivo_cifrado_url": archivo_cifrado_url
    })


@login_required
def index(request):
    midi_file = 'media/output.mid'  # Asegúrate de que el archivo se genera correctamente
    return render(request, 'cifrado_musical/index.html', {'midi_file': midi_file})

@login_required
def cifrar_partitura_view(request):
    archivo_cifrado = None
    if request.method == "POST" and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        clave = int(request.POST.get("clave", 3))

        partitura = PartituraCifrada.objects.create(
            usuario=request.user,
            archivo_original=archivo,
            clave=clave,
        )

        # Convertir Path a String
        input_path = str(os.path.join(settings.MEDIA_ROOT, str(partitura.archivo_original.name)))
        output_path = input_path.replace('.mid', '_cifrado.mid')

        try:
            cifrar_partitura(input_path, output_path, clave)
            partitura.archivo_cifrado = str(output_path).replace(str(settings.MEDIA_ROOT), '')
            partitura.save()
            messages.success(request, "✅ Partitura cifrada y guardada correctamente.")
            archivo_cifrado = partitura.archivo_cifrado
        except Exception as e:
            messages.error(request, f"❌ Error al cifrar la partitura: {e}")

    return render(request, "cifrado_musical/cifrar.html", {"archivo_cifrado": archivo_cifrado})


@login_required
def descifrar_partitura_view(request):
    archivo_descifrado = None
    if request.method == "POST" and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        clave = int(request.POST.get("clave", 3))

        partitura = PartituraDescifrada.objects.create(
            usuario=request.user,
            archivo_cifrado=archivo,
            clave=clave,
        )

        # Convertir Path a String
        input_path = str(os.path.join(settings.MEDIA_ROOT, str(partitura.archivo_cifrado.name)))
        output_path = input_path.replace('.mid', '_descifrado.mid')

        try:
            descifrar_partitura(input_path, output_path, clave)
            partitura.archivo_descifrado = str(output_path).replace(str(settings.MEDIA_ROOT), '')
            partitura.save()
            messages.success(request, "✅ Partitura descifrada y guardada correctamente.")
        except Exception as e:
            messages.error(request, f"❌ Error al descifrar la partitura: {e}")

    return render(request, "cifrado_musical/descifrar.html", {"archivo_descifrado": archivo_descifrado})

@login_required
def historial_partituras_view(request):
    datos = PartituraCifrada.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'cifrado_musical/historial.html', {'datos': datos})
