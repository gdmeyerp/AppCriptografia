from django.db import models
from django.contrib.auth.models import User

# Tabla para almacenar mensajes cifrados con Cifrado de ElGamal
class ElGamalCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_original = models.TextField()
    mensaje_cifrado1 = models.TextField()
    mensaje_cifrado2 = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado - {self.fecha_creacion}"


# Tabla para almacenar mensajes descifrados con Cifrado de ElGamal
class ElGamalDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_cifrado1 = models.TextField()
    mensaje_cifrado2 = models.TextField()
    mensaje_descifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado - {self.fecha_creacion}"



