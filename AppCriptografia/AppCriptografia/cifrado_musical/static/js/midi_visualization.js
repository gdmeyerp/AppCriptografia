// midi_visualization.js
// Funciones para visualizar el contenido musical (cadena de notas y partitura)
// Se asume que VexFlow está cargado

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
    const cadenaNotasDiv = document.getElementById("midi-notes");
    if (cadenaNotasDiv) {
      cadenaNotasDiv.innerHTML = `<strong>Notas detectadas:</strong><br>${notasAgrupadas.join("<br>")}`;
    }
  }

  function mostrarCadenaDeNotasDesplazadas(midi, clave) {
    let notasDesplazadas = [];
    midi.tracks.forEach(track => {
      track.notes.forEach(note => {
        // Se aplica el desplazamiento a cada nota usando la función shiftNote
        notasDesplazadas.push(shiftNote(note.name, clave));
      });
    });
    let notasAgrupadas = [];
    for (let i = 0; i < notasDesplazadas.length; i += 10) {
      notasAgrupadas.push(notasDesplazadas.slice(i, i + 10).join(" - "));
    }
    const cadenaNotasDiv = document.getElementById("midi-notes-desplazadas");
    if (cadenaNotasDiv) {
      cadenaNotasDiv.innerHTML = `<strong>Notas desplazadas:</strong><br>${notasAgrupadas.join("<br>")}`;
    }
  }
  
  
  function visualizarPartitura(midi) {
    if (typeof Vex === "undefined") {
      console.error("❌ VexFlow no está definido.");
      return;
    }
  
    const partituraDiv = document.getElementById("midi-sheet");
    partituraDiv.innerHTML = "";
    const VF = Vex.Flow;
  
    let timeSignatures = midi.header.timeSignatures;
    let timeSig = timeSignatures.length > 0 ? timeSignatures[0].timeSignature : [4, 4];
    let keySig = midi.header.keySignatures.length > 0 ? midi.header.keySignatures[0].key : 'C';
  
    console.log("Tonalidad detectada:", keySig, "  Métrica:", timeSig.join("/"));
  
    let todasNotas = [];
    midi.tracks.forEach(track => {
      track.notes.forEach(note => {
        let vexflowKey = convertirNotaVexFlow(note.name, note.octave);
        let vexflowDuracion = obtenerDuracionVexflow(note.duration);
  
        let staveNote = new VF.StaveNote({
          keys: [vexflowKey],
          duration: vexflowDuracion
        });
  
        if (vexflowKey.includes("#")) {
          staveNote.addModifier(new VF.Accidental("#"), 0);
        } else if (vexflowKey.includes("b")) {
          staveNote.addModifier(new VF.Accidental("b"), 0);
        }
  
        todasNotas.push({ note: staveNote, time: note.time });
      });
    });
  
    // Ordenar las notas por tiempo
    todasNotas.sort((a, b) => a.time - b.time);
  
    // Agrupar las notas en compases
    const measureDuration = timeSig[0];
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
  
    // Configuración de la partitura
    const compasesPorLinea = 2;
    const anchoCompas = 400;
    const separacionVerticalLineas = 130;
    const posXInicial = 10;
    const posYInicial = 50;
  
    const totalCompases = measures.length;
    const totalLineas = Math.ceil(totalCompases / compasesPorLinea);
  
    const rendererWidth = (compasesPorLinea * anchoCompas) + 100;
    const rendererHeight = (totalLineas * separacionVerticalLineas) + 200;
  
    const renderer = new VF.Renderer(partituraDiv, VF.Renderer.Backends.SVG);
    renderer.resize(rendererWidth, rendererHeight);
    const context = renderer.getContext();
  
    // Dibujar cada compás
    measures.forEach((compas, index) => {
      const indiceEnLinea = index % compasesPorLinea;
      const lineaActual = Math.floor(index / compasesPorLinea);
  
      const x = posXInicial + (indiceEnLinea * anchoCompas);
      const y = posYInicial + (lineaActual * separacionVerticalLineas);
  
      // Crear pentagrama
      const stave = new VF.Stave(x, y, anchoCompas);
      if (index === 0) {
        stave.addClef("treble");
        stave.addKeySignature(keySig);
        stave.addTimeSignature(`${timeSig[0]}/${timeSig[1]}`);
      } else {
        stave.setBegBarType(VF.Barline.type.SINGLE);
      }
      stave.setContext(context).draw();
  
      let voice = new VF.Voice({
        num_beats: timeSig[0],
        beat_value: timeSig[1]
      });
      voice.setStrict(false);
  
      // CORRECCIÓN: usamos "compas" en lugar de "compases"
      voice.addTickables(compas);
  
      new VF.Formatter().joinVoices([voice]).format([voice], anchoCompas - 20);
      voice.draw(context, stave);
  
      // Generar beams para notas rápidas
      let beamNotes = compas.filter(n => ["8", "16", "32", "8d"].includes(n.duration));
      if (beamNotes.length > 1) {
        let beams = VF.Beam.generateBeams(beamNotes);
        beams.forEach(b => b.setContext(context).draw());
      }
    });
  
    // Ajustar scroll en el contenedor
    const partituraContainer = document.getElementById("midi-sheet-container");
    if (partituraContainer) {
      partituraContainer.style.overflowX = "scroll";
      partituraContainer.style.overflowY = "scroll";
      partituraContainer.style.maxHeight = "600px";
    }
  }
  
  
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
  