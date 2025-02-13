document.addEventListener("DOMContentLoaded", function () {
  let midiFile = null;
  let midiSynth = null;

  // Elementos HTML
  const archivoInput = document.getElementById("archivo-midi");
  const reproductorContainer = document.getElementById("midi-player");
  const playMidiBtn = document.getElementById("play-midi");
  const stopMidiBtn = document.getElementById("stop-midi");
  const notacionContainer = document.getElementById("midi-notes-container");
  const cadenaNotasDiv = document.getElementById("midi-notes");
  const partituraContainer = document.getElementById("midi-sheet-container");
  const partituraDiv = document.getElementById("midi-sheet");

  // 1️⃣ Carga del Archivo MIDI
  archivoInput.addEventListener("change", function (event) {
    let file = event.target.files[0];
    if (file) {
      let reader = new FileReader();
      reader.onload = async function (e) {
        try {
          midiFile = new Midi(e.target.result);
          reproductorContainer.style.display = "block";
          partituraContainer.style.display = "block";
          notacionContainer.style.display = "block";
          console.log("✅ Archivo MIDI cargado correctamente.");
          if (document.getElementById("midi-encryption-container")) {
            document.getElementById("midi-encryption-container").style.display = "block";
        }
        
          // Mostrar la cadena de notas
          mostrarCadenaDeNotas(midiFile);

          // Dibujar la partitura con ajustes de tonalidad y métrica desde el MIDI
          visualizarPartitura(midiFile);
        } catch (error) {
          console.error("❌ Error al cargar el archivo MIDI:", error);
        }
      };
      reader.readAsArrayBuffer(file);
    }
  });

  // ---------------------
  // Reproducción MIDI
  // ---------------------
  playMidiBtn.addEventListener("click", async function () {
    await Tone.start();
    if (!midiFile) {
      alert("Por favor, carga un archivo MIDI primero.");
      return;
    }

    Tone.Transport.stop();
    Tone.Transport.cancel(0);
    Tone.Transport.position = 0;

    midiSynth = new Tone.PolySynth(Tone.Synth).toDestination();

    midiFile.tracks.forEach(track => {
      track.notes.forEach(note => {
        Tone.Transport.schedule(time => {
          midiSynth.triggerAttack(note.name, time);
          Tone.Transport.schedule(releaseTime => {
            midiSynth.triggerRelease(note.name, releaseTime);
          }, note.time + note.duration);
        }, note.time);
      });
    });

    Tone.Transport.start("+0.1");
    console.log("▶ Reproduciendo MIDI...");
  });

  // ---------------------
  // Detener Reproducción
  // ---------------------
  stopMidiBtn.addEventListener("click", function () {
    if (midiSynth) {
      Tone.Transport.stop();
      Tone.Transport.cancel(0);
      midiSynth.releaseAll();
      console.log("⏹ Reproducción detenida.");
    }
  });

  // Duplicado de stop
  stopMidiBtn.addEventListener("click", function () {
    if (midiSynth) {
      Tone.Transport.stop();
      console.log("⏹ Reproducción detenida.");
    }
  });

  // 4️⃣ Mostrar cadena de notas
  function mostrarCadenaDeNotas(midi) {
    let notas = [];
    midi.tracks.forEach(track => {
      track.notes.forEach(note => {
        notas.push(note.name);
      });
    });
    let notasAgrupadas = [];
    for (let i = 0; i < notas.length; i += 10) {
      notasAgrupadas.push(notas.slice(i, i + 10).join(" - "));
    }
    cadenaNotasDiv.innerHTML = `<strong>Notas detectadas:</strong><br>${notasAgrupadas.join("<br>")}`;
  }

  // ---------------------
  // Visualizar Partitura
  // ---------------------
  function visualizarPartitura(midi) {
    if (typeof Vex === "undefined") {
      console.error("❌ VexFlow no está definido.");
      return;
    }
    partituraDiv.innerHTML = "";

    const VF = Vex.Flow;

    // 1️⃣ Detectar métricas y tonalidad del MIDI (si existen)
    let timeSignatures = midi.header.timeSignatures;
    let timeSig = timeSignatures.length > 0 
      ? timeSignatures[0].timeSignature // [numerator, denominator]
      : [4, 4];

    let keySig = midi.header.keySignatures.length > 0 
      ? midi.header.keySignatures[0].key 
      : 'C';

    console.log("Tonalidad detectada:", keySig, "  Métrica:", timeSig.join("/"));

    // 2️⃣ Recolectar todas las notas -> { note: StaveNote, time: number }
    let todasNotas = [];
    midi.tracks.forEach(track => {
      track.notes.forEach(note => {
        let vexflowKey = convertirNotaVexFlow(note.name, note.octave);
        let vexflowDuracion = obtenerDuracionVexflow(note.duration);

        let staveNote = new VF.StaveNote({
          keys: [vexflowKey],
          duration: vexflowDuracion
        });

        // Accidentals
        if (vexflowKey.includes("#")) {
          staveNote.addModifier(new VF.Accidental("#"), 0);
        } else if (vexflowKey.includes("b")) {
          staveNote.addModifier(new VF.Accidental("b"), 0);
        }

        todasNotas.push({ note: staveNote, time: note.time });
      });
    });

    // 3️⃣ Ordenar por tiempo
    todasNotas.sort((a, b) => a.time - b.time);

    // 4️⃣ Agrupar en compases
    const measureDuration = timeSig[0]; // p.ej. si es 3/4 => measureDuration=3
    let measuresObj = {};

    todasNotas.forEach(item => {
      let measureIndex = Math.floor(item.time / measureDuration);
      if (!measuresObj[measureIndex]) {
        measuresObj[measureIndex] = [];
      }
      measuresObj[measureIndex].push(item.note);
    });

    let measures = Object.keys(measuresObj)
      .sort((a, b) => parseInt(a) - parseInt(b))
      .map(k => measuresObj[k]);

    // 5️⃣ Parámetros para dibujar varios compases por línea
    const compasesPorLinea = 2;        // Por ejemplo, 2 compases por línea
    const anchoCompas = 400;           // 400px para cada compás
    const separacionVerticalLineas = 130;
    const posXInicial = 10;
    const posYInicial = 50;

    // 6️⃣ Calcular cuántos compases totales y cuántas líneas
    const totalCompases = measures.length;
    const totalLineas = Math.ceil(totalCompases / compasesPorLinea);

    // Ancho = compasesPorLinea * anchoCompas + margen
    // Alto  = totalLineas * separacionVerticalLineas + márgenes
    const rendererWidth = (compasesPorLinea * anchoCompas) + 100;
    const rendererHeight = (totalLineas * separacionVerticalLineas) + 200;

    // Crear renderer con ese tamaño dinámico
    const renderer = new VF.Renderer(partituraDiv, VF.Renderer.Backends.SVG);
    renderer.resize(rendererWidth, rendererHeight);
    const context = renderer.getContext();

    // 7️⃣ Dibujar los compases
    measures.forEach((compas, index) => {
      const indiceEnLinea = index % compasesPorLinea;
      const lineaActual = Math.floor(index / compasesPorLinea);

      const x = posXInicial + (indiceEnLinea * anchoCompas);
      const y = posYInicial + (lineaActual * separacionVerticalLineas);

      // Crear pentagrama
      const stave = new VF.Stave(x, y, anchoCompas);
      // Solo en el primer compás
      if (index === 0) {
        stave.addClef("treble");
        stave.addKeySignature(keySig);
        stave.addTimeSignature(`${timeSig[0]}/${timeSig[1]}`);
      } else {
        stave.setBegBarType(VF.Barline.type.SINGLE);
      }
      stave.setContext(context).draw();

      // Voice
      let voice = new VF.Voice({ 
        num_beats: timeSig[0],
        beat_value: timeSig[1]
      });
      voice.setStrict(false);
      voice.addTickables(compas);

      new VF.Formatter().joinVoices([voice]).format([voice], anchoCompas - 20);
      voice.draw(context, stave);

      // Beams
      let beamNotes = compas.filter(n => ["8", "16", "32", "8d"].includes(n.duration));
      if (beamNotes.length > 1) {
        let beams = VF.Beam.generateBeams(beamNotes);
        beams.forEach(b => b.setContext(context).draw());
      }
    });

    // 8️⃣ Ajustar scroll
    partituraContainer.style.overflowX = "scroll";
    partituraContainer.style.overflowY = "scroll";
    partituraContainer.style.maxHeight = "600px";
  }

  // Funciones auxiliares
  function convertirNotaVexFlow(nota, octava) {
    let base = nota.replace(/\d+/g, "");
    if (!base.match(/^[A-Ga-g](#|b)?$/)) {
      console.error("❌ Nota inválida detectada:", nota);
      return "C/4";
    }
    return base.replace("♯", "#").replace("♭", "b") + "/" + octava;
  }

  function obtenerDuracionVexflow(duracion) {
    if (duracion >= 1) return "w";
    if (duracion >= 0.5) return "h";
    if (duracion >= 0.25) return "q";
    if (duracion >= 0.125) return "8";
    return "16";
  }
});
