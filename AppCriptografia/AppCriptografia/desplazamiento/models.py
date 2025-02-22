from django.db import models
from django.contrib.auth.models import User

# Tabla para almacenar mensajes cifrados con Desplazamiento
class DesplazamientoCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_original = models.TextField()
    clave = models.IntegerField()  # Clave de desplazamiento
    mensaje_cifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado por desplazamiento - {self.fecha_creacion}"


# Tabla para almacenar mensajes descifrados con Desplazamiento
class DesplazamientoDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_cifrado = models.TextField()
    clave = models.IntegerField()  # Clave de desplazamiento
    mensaje_descifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado por desplazamiento - {self.fecha_creacion}"
