// midi_backend.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  

// window.encryptedNotes contiene el arreglo de notas encriptadas
async function enviarNotasEncriptadas() {
    const response = await fetch('/cifrado_musical/crear_midi/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') 
      },
      body: JSON.stringify({
        encryptedNotes: window.encryptedNotes,
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      window.location.href = data.url;
    } else {
      console.error("Error al enviar las notas encriptadas");
    }
  }
  
