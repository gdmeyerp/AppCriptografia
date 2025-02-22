// midi_encryption.js
// Funciones de encriptación

// Método 1: Desplazamiento (shift)
function shiftNote(noteStr, shift) {
  const regex = /^([A-G][#b]?)(\d+)$/;
  const match = noteStr.match(regex);
  if (!match) {
    console.error("Formato de nota inválido:", noteStr);
    return noteStr;
  }
  let notePart = match[1];
  let octave = parseInt(match[2]);
  const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  let index = notes.indexOf(notePart);
  if (index === -1) {
    console.error("Nota no encontrada en array:", notePart);
    return noteStr;
  }
  let newIndex = index + shift;
  while (newIndex < 0) {
    newIndex += 12;
    octave -= 1;
  }
  while (newIndex >= 12) {
    newIndex -= 12;
    octave += 1;
  }
  return notes[newIndex] + octave;
}

function encryptDesplazamiento(midi, clave) {
  let encryptedNotes = [];
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      let shifted = shiftNote(note.name, clave);
      encryptedNotes.push(shifted);
    });
  });
  return encryptedNotes;
}

// Método 2: Retroceso
function encryptRetroceso(midi) {
  let allNotes = [];
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      allNotes.push(note.name);
    });
  });
  return allNotes.reverse();
}

// Método 3: Inversión
function noteToSemitone(noteStr) {
  const regex = /^([A-G][#b]?)(\d+)$/;
  const match = noteStr.match(regex);
  if (!match) {
    console.error("Formato de nota inválido:", noteStr);
    return 0;
  }
  const notePart = match[1];
  const octave = parseInt(match[2]);
  const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const index = notes.indexOf(notePart);
  if (index === -1) {
    console.error("Nota no encontrada:", notePart);
    return 0;
  }
  return octave * 12 + index;
}

function semitoneToNote(semi) {
  const octave = Math.floor(semi / 12);
  const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const index = semi % 12;
  return notes[index] + octave;
}

function encryptInversion(midi, pivotStr) {
  let pivotSemi = noteToSemitone(pivotStr);
  let encryptedNotes = [];
  midi.tracks.forEach(track => {
    track.notes.forEach(note => {
      let noteSemi = noteToSemitone(note.name);
      let invertedSemi = 2 * pivotSemi - noteSemi;
      let invertedNote = semitoneToNote(invertedSemi);
      encryptedNotes.push(invertedNote);
    });
  });
  return encryptedNotes;
}

// Función para crear módulos (cards) de forma dinámica
function crearModuloDinamico(config) {
  const {
    id,
    headerHTML,
    bodyHTML,
    cardClasses = "card shadow",
    headerClasses = "card-header bg-info text-white text-center",
    bodyClasses = "card-body",
    parentContainerId = "midi-encryption-container"
  } = config;
  
  // Crear contenedor principal
  const container = document.createElement("div");
  container.className = cardClasses;
  container.style.display = "block";
  container.id = id;

  // Crear header y asignarle contenido
  const header = document.createElement("div");
  header.className = headerClasses;
  header.innerHTML = headerHTML;

  // Crear body y asignarle contenido
  const body = document.createElement("div");
  body.className = bodyClasses;
  body.innerHTML = bodyHTML;

  // Agregar header y body al contenedor principal
  container.appendChild(header);
  container.appendChild(body);

  // Insertar el módulo en el DOM dentro del contenedor padre (o en el body como alternativa)
  const parentContainer = document.getElementById(parentContainerId) || document.body;
  // Si existe un módulo previo con el mismo ID, eliminarlo
  const existingModule = document.getElementById(id);
  if (existingModule) {
    parentContainer.removeChild(existingModule);
  }
  parentContainer.appendChild(container);
  
  return container;
}

// Función que procesa la encriptación y crea las vistas para notas encriptadas y originales
function aplicarEncriptacionFrontend(midi) {
  // 1. Obtener el método de encriptación seleccionado y calcular las notas encriptadas.
  const metodo = document.getElementById("metodoEncriptacion").value;
  let encryptedNotes;

  if (metodo === "desplazamiento") {
    const clave = parseInt(document.getElementById("claveDesplazamiento").value) || 3;
    encryptedNotes = encryptDesplazamiento(midi, clave);
  } else if (metodo === "retroceso") {
    encryptedNotes = encryptRetroceso(midi);
  } else if (metodo === "inversion") {
    const pivot = document.getElementById("pivotNote") ? document.getElementById("pivotNote").value : "C4";
    encryptedNotes = encryptInversion(midi, pivot);
  } else {
    console.error("Método de encriptación no reconocido:", metodo);
    return;
  }

  // **Asignamos el arreglo de notas encriptadas a una variable global**
  window.encryptedNotes = encryptedNotes;

  console.log("Ejecutando encriptación con método:", metodo, "Resultado:", encryptedNotes);

  // 3. Extraer las notas originales del objeto MIDI.
  let originalNotes = [];
  if (midi.tracks) {
    midi.tracks.forEach(track => {
      track.notes.forEach(note => {
        originalNotes.push(note.name);
      });
    });
  }
  if (originalNotes.length === 0) {
    originalNotes.push("No se encontraron notas originales.");
  }
  
  // 4. Crear la vista para las notas originales.
  crearModuloDinamico({
    id: "midi-notes-original-container-dinamico",
    headerHTML: `<h5 class="mb-0"><i class="fas fa-music"></i> Notación de Notas Originales</h5>`,
    bodyHTML: `<p><strong>Notas originales:</strong><br>${originalNotes.join(" - ")}</p>`,
    cardClasses: "card shadow mb-3",
    headerClasses: "card-header bg-secondary text-white text-center",
    bodyClasses: "card-body",
    parentContainerId: "midi-encryption-container"
  });

  // 2. Crear la vista para las notas encriptadas.
  crearModuloDinamico({
    id: "midi-notes-encriptadas-container-dinamico",
    headerHTML: `<h5 class="mb-0"><i class="fas fa-lock"></i> Notación de Notas (Encriptadas)</h5>`,
    bodyHTML: `<p><strong>Notas encriptadas:</strong><br>${encryptedNotes.join(" - ")}</p>`,
    cardClasses: "card shadow mb-3",
    headerClasses: "card-header bg-info text-white text-center",
    bodyClasses: "card-body",
    parentContainerId: "midi-encryption-container"
  });
}


// Exportar para uso global
window.aplicarEncriptacionFrontend = aplicarEncriptacionFrontend;

// --- Control de parámetros del método de encriptación ---
// Al cambiar el método seleccionado se muestran/ocultan los parámetros correspondientes.
document.addEventListener("DOMContentLoaded", function() {
  const metodoSelect = document.getElementById("metodoEncriptacion");
  if (metodoSelect) {
    metodoSelect.addEventListener("change", function() {
      // Oculta ambos bloques de parámetros
      const divDesplazamiento = document.getElementById("parametros-desplazamiento");
      const divInversion = document.getElementById("parametros-inversion");
      if (divDesplazamiento) divDesplazamiento.style.display = "none";
      if (divInversion) divInversion.style.display = "none";

      // Según el método, muestra el bloque correspondiente
      if (this.value === "desplazamiento") {
        if (divDesplazamiento) divDesplazamiento.style.display = "block";
      } else if (this.value === "inversion") {
        if (divInversion) divInversion.style.display = "block";
      }
      // Para "retroceso" no se requiere parámetro adicional.
    });
    // Disparar el evento para establecer la visualización inicial
    metodoSelect.dispatchEvent(new Event("change"));
  }

  
});
