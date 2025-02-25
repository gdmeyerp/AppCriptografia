from django.db import models
from django.contrib.auth.models import User

class RsaCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje_original = models.TextField()
    mensaje_cifrado = models.TextField()
    clave_publica = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado - {self.fecha_creacion}"

class RsaDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje_cifrado = models.TextField()
    mensaje_descifrado = models.TextField()
    clave_privada = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado - {self.fecha_creacion}"
