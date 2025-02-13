document.addEventListener("DOMContentLoaded", function () {
    console.log("🔄 Cargando encryption_handler.js...");

    const metodoSelect = document.getElementById("metodoEncriptacion");
    const btnAplicar = document.getElementById("btn-aplicar-encriptacion");
    const encryptionContainer = document.getElementById("midi-encryption-container");

    // Contenedores de salida de encriptación
    const encryptedNotesContainer = document.getElementById("midi-encrypted-notes-container");
    const encryptedNotesDiv = document.getElementById("midi-encrypted-notes");
    const encryptedSheetContainer = document.getElementById("midi-encrypted-sheet-container");
    const encryptedSheetDiv = document.getElementById("midi-encrypted-sheet");

    if (!metodoSelect || !btnAplicar || !encryptionContainer) {
        console.error("❌ No se encontró uno o más elementos de encriptación en el HTML.");
        return;
    }

    // Aplicar Encriptación
    btnAplicar.addEventListener("click", function () {
        const metodo = metodoSelect.value;
        let params = {};

        switch (metodo) {
            case "desplazamiento":
                params.clave = parseInt(document.getElementById("clave").value) || 3;
                break;
            case "inversion":
                params.nota_pivote = document.getElementById("notaPivote").value || "C4";
                break;
            case "ruido_aleatorio":
                params.intensidad = parseInt(document.getElementById("ruidoIntensidad").value) || 1;
                break;
            case "compresion_temporal":
                params.factor = parseFloat(document.getElementById("factorCompresion").value) || 0.8;
                break;
            case "enmascaramiento_armonico":
                params.intervalo = document.getElementById("intervaloArm").value || "P5";
                break;
            case "retroceso":
                break;
            default:
                console.warn("Método no reconocido.");
                return;
        }

        console.log("🔐 Aplicando encriptación con método:", metodo, "y parámetros:", params);

        fetch("/encriptar_midi/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCSRFToken(),
            },
            body: JSON.stringify({ metodo, ...params }),
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.success) {
                console.log("✅ Encriptación completada:", data);
                alert("Encriptación realizada con éxito. Notas y partitura generadas.");

                // Mostrar la sección de notas encriptadas
                encryptedNotesContainer.style.display = "block";
                encryptedNotesDiv.innerHTML = `<strong>Notas encriptadas:</strong><br>${data.notas.join(" - ")}`;

                // Mostrar la partitura encriptada
                encryptedSheetContainer.style.display = "block";
                visualizarPartituraEncriptada(data.midi_encriptado);

            } else {
                alert("❌ Error: " + data.error);
            }
        })
        .catch(err => console.error("❌ Error en la encriptación:", err));
    });

    function obtenerCSRFToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
        return cookieValue || "";
    }

    function visualizarPartituraEncriptada(midiData) {
        if (typeof Vex === "undefined") {
            console.error("❌ VexFlow no está definido.");
            return;
        }
        encryptedSheetDiv.innerHTML = "";

        const VF = Vex.Flow;

        const renderer = new VF.Renderer(encryptedSheetDiv, VF.Renderer.Backends.SVG);
        renderer.resize(800, 300);
        const context = renderer.getContext();
        const stave = new VF.Stave(10, 40, 700);
        stave.addClef("treble").setContext(context).draw();

        let notes = midiData.map(note => new VF.StaveNote({
            keys: [note],
            duration: "q"
        }));

        let voice = new VF.Voice({ num_beats: 4, beat_value: 4 });
        voice.addTickables(notes);
        new VF.Formatter().joinVoices([voice]).format([voice], 700);
        voice.draw(context, stave);
    }
});
