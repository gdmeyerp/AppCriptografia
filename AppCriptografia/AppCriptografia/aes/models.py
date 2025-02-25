from django.db import models
from django.contrib.auth.models import User

class ImagenCifradaAES(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Usuario relacionado
    imagen_original = models.ImageField(upload_to='imagenes/originales/')
    clave = models.CharField(max_length=32) #Clave DES tiene que tener 16,24 o 32 bytes
    imagen_cifrada = models.ImageField(upload_to='imagenes/cifradas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Imagen - {self.id} - Cifrado - {self.fecha_creacion}"

class ImagenDescifradaAES(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Usuario relacionado
    imagen_cifrada = models.ImageField(upload_to='imagenes/cifradas/')
    clave = models.CharField(max_length=32) #Clave AES tiene que tener 16,24 o 32 bytes
    imagen_descifrada = models.ImageField(upload_to='imagenes/descifradas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Imagen Cifrada - {self.id} - Descifrado - {self.fecha_creacion}"
 