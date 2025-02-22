// midi_backend.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Cada cookie se escribe en la forma "name=value"
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  

// Supongamos que window.encryptedNotes contiene el arreglo de notas encriptadas
async function enviarNotasEncriptadas() {
    const response = await fetch('/cifrado_musical/crear_midi/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  // si usas Django y CSRF protection
      },
      body: JSON.stringify({
        encryptedNotes: window.encryptedNotes,
        // Puedes enviar más información si es necesario, p.ej., tempo, firmas, etc.
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      // data.url puede ser la URL para descargar el archivo MIDI generado
      window.location.href = data.url;
    } else {
      console.error("Error al enviar las notas encriptadas");
    }
  }
  
