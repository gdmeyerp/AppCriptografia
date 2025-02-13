from django.db import models
from django.contrib.auth.models import User

# Tabla para almacenar mensajes cifrados con Cifrado de Permutación
class PermutacionCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_original = models.TextField()
    clave = models.CharField(max_length=255)
    mensaje_cifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado - {self.fecha_creacion}"


# Tabla para almacenar mensajes descifrados con Cifrado de Permutación
class PermutacionDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_cifrado = models.TextField()
    clave = models.CharField(max_length=255)
    mensaje_descifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado - {self.fecha_creacion}"

class PermutacionMensajeCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje_original = models.TextField()
    clave = models.CharField(max_length=255)
    mensaje_cifrado = models.TextField()
    metodo = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.metodo} - {self.fecha_creacion}"

