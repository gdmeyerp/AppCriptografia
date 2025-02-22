from django.db import models
from django.contrib.auth.models import User

class PartituraCifrada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo_original = models.FileField(upload_to='partituras/originales/')
    clave = models.IntegerField()
    archivo_cifrado = models.FileField(upload_to='partituras/cifradas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado - {self.fecha_creacion}"

class PartituraDescifrada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo_cifrado = models.FileField(upload_to='partituras/cifradas/')
    clave = models.IntegerField()
    archivo_descifrado = models.FileField(upload_to='partituras/descifradas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado - {self.fecha_creacion}"
