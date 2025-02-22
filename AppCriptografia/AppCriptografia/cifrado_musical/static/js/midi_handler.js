// midi_handler.js
// Funcionalidades generales: lectura del archivo MIDI, control de reproducción y manejo de eventos

document.addEventListener("DOMContentLoaded", function () {
  let midiFile = null;      // MIDI original parseado
  let midiSynth = null;     // Sintetizador Tone.js
  window.midiEncriptado = null;  // MIDI encriptado (global)

  // Elementos HTML
  const archivoInput = document.getElementById("archivo-midi");
  const reproductorContainer = document.getElementById("midi-player");
  const playMidiBtn = document.getElementById("play-midi");
  const stopMidiBtn = document.getElementById("stop-midi");

  // =====================================================
  // 1. Manejar la carga del archivo (se encripta automáticamente)
  // =====================================================
  function handleFileAndEncrypt(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = async function (e) {
        try {
          // 1. Parsear el archivo MIDI original
          midiFile = new Midi(e.target.result);
          reproductorContainer.style.display = "block";

          // 2. Visualización de notas y partitura
          if (typeof mostrarCadenaDeNotas === "function") {
            mostrarCadenaDeNotas(midiFile);
          }
          if (typeof visualizarPartitura === "function") {
            visualizarPartitura(midiFile);
          }
          if (typeof mostrarCadenaDeNotasDesplazadas === "function") {
            // Muestra un ejemplo de desplazamiento a +3 semitonos
            mostrarCadenaDeNotasDesplazadas(midiFile, 3);
          }
          console.log("✅ Archivo MIDI cargado correctamente.");

          // 3. Aplicar encriptación por defecto (ya definida en midi_encryption.js)
          if (typeof aplicarEncriptacionFrontend === "function") {
            aplicarEncriptacionFrontend(midiFile);  // Esto genera window.encryptedNotes
          }

          // 4. Construir el objeto MIDI encriptado (usando las notas encriptadas)
          if (window.encryptedNotes && typeof generarMidiEncriptado === "function") {
            window.midiEncriptado = generarMidiEncriptado(midiFile, window.encryptedNotes);
            console.log("✅ MIDI encriptado generado automáticamente.");
          } else {
            console.warn("⚠ No se generaron notas encriptadas. handleFileAndEncrypt");
            window.midiEncriptado = null;
          }

        } catch (error) {
          console.error("❌ Error al cargar el archivo MIDI:", error);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  }
  window.handleFileAndEncrypt = handleFileAndEncrypt;


  // =====================================================
  // 3. Reproducción MIDI con los botones "play" y "stop"
  // =====================================================
  playMidiBtn.addEventListener("click", async function () {
    await Tone.start();

    // Se decide cuál MIDI reproducir:
    //  - Prioridad: si existe un MIDI encriptado, reproducirlo.
    //  - Caso contrario: reproducir el MIDI original.
    const midiToPlay = window.midiEncriptado || midiFile;

    if (!midiToPlay) {
      alert("Por favor, carga un archivo MIDI primero.");
      return;
    }

    // Preparar el Transport
    Tone.Transport.stop();
    Tone.Transport.cancel(0);
    Tone.Transport.position = 0;

    // Crear sintetizador
    midiSynth = new Tone.PolySynth(Tone.Synth).toDestination();

    // Programar las notas
    midiToPlay.tracks.forEach(track => {
      track.notes.forEach(note => {
        Tone.Transport.schedule(time => {
          midiSynth.triggerAttack(note.name, time);
          Tone.Transport.schedule(releaseTime => {
            midiSynth.triggerRelease(note.name, releaseTime);
          }, note.time + note.duration);
        }, note.time);
      });
    });

    // Iniciar transporte
    Tone.Transport.start("+0.1");
    console.log("▶ Reproduciendo MIDI...");
  });

  stopMidiBtn.addEventListener("click", function () {
    if (midiSynth) {
      Tone.Transport.stop();
      Tone.Transport.cancel(0);
      midiSynth.releaseAll();
      console.log("⏹ Reproducción detenida.");
    }
  });
  
  // (Opcional) Duplicado de stop (si lo deseas conservar)
  stopMidiBtn.addEventListener("click", function () {
    if (midiSynth) {
      Tone.Transport.stop();
      console.log("⏹ Reproducción detenida.");
    }
  });
});
