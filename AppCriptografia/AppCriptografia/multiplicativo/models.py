from django.db import models
from django.contrib.auth.models import User

class MultiplicativoCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje_original = models.TextField()
    mensaje_cifrado = models.TextField()
    clave = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado - {self.fecha_creacion}"

class MultiplicativoDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje_cifrado = models.TextField()
    mensaje_descifrado = models.TextField()
    clave = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado - {self.fecha_creacion}"
