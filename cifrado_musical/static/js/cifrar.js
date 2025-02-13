// ✅ Módulo principal para la gestión de archivos MIDI
const MidiManager = (() => {
    let midiOriginal = null;
    let midiSynth = null;
    let midiCifrado = null;
    let midiCifradoSynth = null;

    // Elementos HTML
    const archivoInput = document.getElementById("archivo");
    const reproductorContainer = document.getElementById("reproductor-container");
    const playMidiBtn = document.getElementById("play-midi");
    const stopMidiBtn = document.getElementById("stop-midi");
    const playMidiCifradoBtn = document.getElementById("play-midi-cifrado");
    const stopMidiCifradoBtn = document.getElementById("stop-midi-cifrado");
    const partituraOriginalContainer = document.getElementById("partitura-original");
    const partituraCifradaContainer = document.getElementById("partitura-cifrada");

    // ✅ 1️⃣ Inicializa los eventos
    const init = () => {
        if (!archivoInput || !reproductorContainer) return;

        // Restaurar estado del reproductor si ya estaba visible antes
        if (localStorage.getItem("reproductorVisible") === "true") {
            reproductorContainer.style.display = "block";
        }

        archivoInput.addEventListener("change", handleFileUpload);
        playMidiBtn?.addEventListener("click", playOriginalMidi);
        stopMidiBtn?.addEventListener("click", stopOriginalMidi);
        playMidiCifradoBtn?.addEventListener("click", playEncryptedMidi);
        stopMidiCifradoBtn?.addEventListener("click", stopEncryptedMidi);
    };

    // ✅ 2️⃣ Maneja la carga del archivo MIDI
    const handleFileUpload = (event) => {
        let file = event.target.files[0];

        if (file) {
            let reader = new FileReader();
            reader.onload = async function (e) {
                try {
                    clearMidiData(); // Limpia datos previos antes de cargar un nuevo archivo
                    midiOriginal = new Midi(e.target.result);
                    reproductorContainer.style.display = "block";
                    localStorage.setItem("reproductorVisible", "true");
                    console.log("✅ MIDI Original cargado correctamente.");
                    
                    // Visualizar la partitura del MIDI original
                    visualizarPartitura(midiOriginal, partituraOriginalContainer);
                } catch (error) {
                    console.error("❌ Error cargando MIDI:", error);
                }
            };
            reader.readAsArrayBuffer(file);
        }
    };

    // ✅ 3️⃣ Reproducir archivo MIDI original
    const playOriginalMidi = async () => {
        if (!midiOriginal) {
            alert("Por favor, carga un archivo MIDI antes de reproducir.");
            return;
        }

        await Tone.start();
        Tone.Transport.cancel();
        midiSynth = new Tone.PolySynth(Tone.Synth).toDestination();

        midiOriginal.tracks.forEach(track => {
            track.notes.forEach(note => {
                midiSynth.triggerAttackRelease(note.name, note.duration, note.time);
            });
        });

        Tone.Transport.start();
        console.log("▶ Reproduciendo MIDI original...");
        reproductorContainer.style.display = "block";
    };

    // ✅ 4️⃣ Detener la reproducción del MIDI original
    const stopOriginalMidi = () => {
        if (midiSynth) {
            Tone.Transport.stop();
            console.log("⏹ Reproducción detenida.");
        }
    };

    // ✅ 5️⃣ Reproducir archivo MIDI cifrado
    const playEncryptedMidi = async () => {
        let archivoCifrado = playMidiCifradoBtn?.dataset.archivoCifrado;

        if (!archivoCifrado) {
            alert("No hay archivo MIDI cifrado disponible.");
            return;
        }

        console.log("📂 Cargando archivo cifrado:", archivoCifrado);

        try {
            let response = await fetch(archivoCifrado);
            if (!response.ok) throw new Error("❌ No se pudo cargar el archivo MIDI cifrado.");

            let arrayBuffer = await response.arrayBuffer();
            midiCifrado = new Midi(arrayBuffer);

            console.log("✅ Archivo MIDI cifrado cargado correctamente.");

            await Tone.start();
            Tone.Transport.cancel();
            midiCifradoSynth = new Tone.PolySynth(Tone.Synth).toDestination();

            midiCifrado.tracks.forEach(track => {
                track.notes.forEach(note => {
                    midiCifradoSynth.triggerAttackRelease(note.name, note.duration, note.time);
                });
            });

            Tone.Transport.start();
            console.log("▶ Reproduciendo MIDI cifrado...");

            // Visualizar la partitura del MIDI cifrado
            visualizarPartitura(midiCifrado, partituraCifradaContainer);
        } catch (error) {
            console.error("❌ Error al reproducir el archivo MIDI cifrado:", error);
            alert("Error al reproducir el archivo MIDI cifrado.");
        }
    };

    // ✅ 6️⃣ Detener la reproducción del MIDI cifrado
    const stopEncryptedMidi = () => {
        if (midiCifradoSynth) {
            Tone.Transport.stop();
            console.log("⏹ Reproducción del MIDI cifrado detenida.");
        }
    };

    // ✅ 7️⃣ Limpia los datos al cargar un nuevo archivo
    const clearMidiData = () => {
        midiOriginal = null;
        midiSynth = null;
        midiCifrado = null;
        midiCifradoSynth = null;
        Tone.Transport.stop();
    };

    // ✅ 8️⃣ Función para visualizar la partitura con VexFlow
    const visualizarPartitura = (midi, container) => {
        if (!midi || !container) return;

        container.innerHTML = ""; // Limpiar contenido anterior

        const VF = Vex.Flow;
        const renderer = new VF.Renderer(container, VF.Renderer.Backends.SVG);
        renderer.resize(600, 150);
        const context = renderer.getContext();
        const stave = new VF.Stave(10, 40, 500);
        stave.addClef("treble").setContext(context).draw();

        let notes = midi.tracks[0]?.notes.map(note => 
            new VF.StaveNote({
                keys: [`${note.name.toLowerCase()}/4`],
                duration: "q"
            })
        );

        if (!notes || notes.length === 0) {
            console.warn("⚠ No hay notas disponibles para visualizar.");
            return;
        }

        const voice = new VF.Voice({ num_beats: notes.length, beat_value: 4 });
        voice.addTickables(notes);

        const formatter = new VF.Formatter().joinVoices([voice]).format([voice], 400);
        voice.draw(context, stave);
    };

    // ✅ Exponer funciones públicas (por si se necesitan en otros módulos)
    return {
        init,
        playOriginalMidi,
        stopOriginalMidi,
        playEncryptedMidi,
        stopEncryptedMidi,
        handleFileUpload,
        clearMidiData,
        visualizarPartitura
    };
})();

// ✅ Ejecutar la inicialización cuando se cargue la página
document.addEventListener("DOMContentLoaded", MidiManager.init);
