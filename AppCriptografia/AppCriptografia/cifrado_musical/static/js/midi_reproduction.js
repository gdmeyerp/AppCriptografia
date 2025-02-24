// midi_reproduction.js

/**
 * Convierte un nombre de nota (ej: 'C4') a número MIDI (0-127).
 */
function noteToMidi(noteName) {
  const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const note = noteName.replace(/\d+/, '');
  const octave = parseInt(noteName.match(/\d+/)[0]);
  const semitone = notes.indexOf(note);
  if (semitone === -1) return null;
  return semitone + (octave + 1) * 12;
}

/**
 * Genera un nuevo objeto MIDI a partir del original,
 * reemplazando en orden las notas por las encriptadas.
 */
function generarMidiEncriptado(midi, encryptedNotes) {
  // Crear un nuevo objeto MIDI básico con header y tracks
  const midiEncriptado = {
    header: {
      name: midi.header.name,
      tempos: [...midi.header.tempos],
      timeSignatures: [...midi.header.timeSignatures],
      ppq: midi.header.ppq
    },
    tracks: []
  };
  let noteIndex = 0;
  // Copiar cada pista y reemplazar las notas
  midi.tracks.forEach(track => {
    const newTrack = {
      channel: track.channel,
      instrument: track.instrument,
      name: track.name,
      notes: []
    };
    track.notes.forEach(note => {
      if (noteIndex < encryptedNotes.length) {
        const midiNumber = noteToMidi(encryptedNotes[noteIndex]);
        if (midiNumber !== null) {
          newTrack.notes.push({
            duration: note.duration,
            durationTicks: note.durationTicks,
            midi: midiNumber,
            name: encryptedNotes[noteIndex],
            time: note.time,
            velocity: note.velocity
          });
        }
        noteIndex++;
      }
    });
    midiEncriptado.tracks.push(newTrack);
  });
  return midiEncriptado;
}

/**
 * el archivo MIDI a partir del objeto midiEncriptado.
 *
 */
function crearArchivoMidi(midiEncriptado) {
  // Verificar que jsmidgen esté cargado.
  if (typeof Midi === "undefined" || typeof Midi.File === "undefined") {
    console.error("jsmidgen no está cargado.");
    return null;
  }
  
  // Crear un nuevo archivo MIDI
  var file = new Midi.File();
  
  // Crear un track de control para el tempo (y opcionalmente para time signature)
  var controlTrack = new Midi.Track();
  file.addTrack(controlTrack);
  
  // Configurar el tempo: si el header tiene un tempo definido, usarlo; de lo contrario, 120 BPM.
  if (midiEncriptado.header && midiEncriptado.header.tempos && midiEncriptado.header.tempos[0]) {
    var bpm = midiEncriptado.header.tempos[0].bpm;
    controlTrack.setTempo(bpm);
  } else {
    controlTrack.setTempo(120);
  }
    
  // Para cada pista en el objeto MIDI encriptado, crea un track en el archivo
  midiEncriptado.tracks.forEach(function(trk) {
    var track = new Midi.Track();
    file.addTrack(track);
    
    trk.notes.forEach(function(note) {
      // Usamos una duración fija '4' (negra) para cada nota.
      track.addNote(0, note.name, '4');
    });
  });
  
  // Retornar el archivo MIDI como una cadena binaria.
  return file.toBytes();
}

/**
 * Convierte la cadena binaria a un ArrayBuffer y fuerza la descarga del archivo MIDI.
 */
function descargarMidi(midiData) {
  const byteCharacters = midiData; // midiData es una cadena binaria
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], { type: "audio/midi" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "midi_encriptado.mid";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Exportar funciones globalmente
window.generarMidiEncriptado = generarMidiEncriptado;
window.crearArchivoMidi = crearArchivoMidi;
window.descargarMidi = descargarMidi;
