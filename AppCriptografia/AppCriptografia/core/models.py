from django.db import models
from django.contrib.auth.models import User

class HistorialCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    mensaje_original = models.TextField()
    mensaje_cifrado = models.TextField()
    clave = models.CharField(max_length=100)
    metodo = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.metodo}"

