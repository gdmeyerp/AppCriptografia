from music21 import converter, note, chord

def cifrar_partitura(
    input_path, 
    output_path, 
    shift=3
):
    """
    Cifra una partitura desplazando las notas en una clave dada (transposición simple).
    """
    score = converter.parse(input_path)
    
    for part in score.parts:
        for element in part.flatten().notes:
            if element.isNote:
                # Desplazar nota individual
                element.pitch.midi = _aplicar_desplazamiento(element.pitch.midi, shift)
            elif element.isChord:
                # Desplazar cada nota del acorde
                for p in element.pitches:
                    p.midi = _aplicar_desplazamiento(p.midi, shift)
    
    score.write('midi', fp=output_path)

def descifrar_partitura(
    input_path, 
    output_path, 
    shift=3
):
    """
    Descifra la partitura revirtiendo el desplazamiento de notas (transposición inversa).
    """
    # Para descifrar, simplemente se invierte el desplazamiento
    cifrar_partitura(input_path, output_path, -shift)


def cifrar_partitura_avanzada(
    input_path, 
    output_path, 
    shift=3,
    invertir=False,
    pitch_central=60,  # C4 en MIDI
    escalar_duracion=1.0
):
    """
    Cifra una partitura aplicando varias transformaciones:
      - Desplazamiento (shift)
      - Inversión alrededor de un pitch central (invertir)
      - Escalado de la duración (escalar_duracion)
    """
    score = converter.parse(input_path)
    
    for part in score.parts:
        for element in part.flatten().notesAndRests:
            # --- Transformaciones de pitch (notas y acordes) ---
            if element.isNote:
                # Transformar nota individual
                elemento_midi = element.pitch.midi
                elemento_midi = _aplicar_desplazamiento(elemento_midi, shift)
                if invertir:
                    elemento_midi = _aplicar_inversion(elemento_midi, pitch_central)
                # Asignar nuevo valor de pitch clamped (0-127)
                element.pitch.midi = _clamp_midi(elemento_midi)
            elif element.isChord:
                # Transformar cada pitch del acorde
                for i, p in enumerate(element.pitches):
                    p_midi = p.midi
                    p_midi = _aplicar_desplazamiento(p_midi, shift)
                    if invertir:
                        p_midi = _aplicar_inversion(p_midi, pitch_central)
                    element.pitches[i].midi = _clamp_midi(p_midi)

            # --- Transformación de duración (notas o silencios) ---
            # Si es una nota o un silencio, podemos escalar la duración.
            if hasattr(element, 'duration'):
                element.duration.quarterLength *= escalar_duracion

    # Guardar partitura en MIDI
    score.write('midi', fp=output_path)


def descifrar_partitura_avanzada(
    input_path, 
    output_path, 
    shift=3,
    invertir=False,
    pitch_central=60,
    escalar_duracion=1.0
):
    """
    Descifra la partitura revirtiendo las transformaciones aplicadas en cifrar_partitura_avanzada.
      - Se aplica el desplazamiento inverso (shift negativo).
      - Se aplica de nuevo la inversión (invertir) con el mismo pitch central para “deshacer” la inversión.
      - Se escala la duración con el factor inverso (1 / escalar_duracion).
    """
    # Para descifrar, invertimos el desplazamiento y escalamos a la inversa.
    cifrar_partitura_avanzada(
        input_path,
        output_path,
        shift=-shift,
        invertir=invertir,  # La inversión se revierte aplicándola de nuevo con el mismo centro
        pitch_central=pitch_central,
        escalar_duracion=(1.0 / escalar_duracion if escalar_duracion != 0 else 1.0)
    )


# -------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -------------------------------------------------------------------------
def _aplicar_desplazamiento(midi_value, shift):
    """
    Aplica un desplazamiento (transposición) a un valor MIDI.
    """
    return midi_value + shift

def _aplicar_inversion(midi_value, pitch_central):
    """
    Invierte el pitch alrededor de un valor central (pitch_central).
    Si pitch_central = 60 (Do central), y la nota es 64 (Mi), la invertida será:
      2 * 60 - 64 = 56  (Sol#2)
    """
    return 2 * pitch_central - midi_value

def _clamp_midi(midi_value):
    """
    Limita el valor MIDI al rango válido [0..127].
    """
    return max(0, min(127, midi_value))
