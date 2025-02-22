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
