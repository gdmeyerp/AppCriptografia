from django.db import models
from django.contrib.auth.models import User

# Tabla para almacenar mensajes cifrados con Afin
class AfinCifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_original = models.TextField()
    clave_a = models.IntegerField()  # Clave 'a' para el cifrado Afin
    clave_b = models.IntegerField()  # Clave 'b' para el cifrado Afin
    mensaje_cifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Cifrado Afin - {self.fecha_creacion}"


# Tabla para almacenar mensajes descifrados con Afin
class AfinDescifrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario relacionado
    mensaje_cifrado = models.TextField()
    clave_a = models.IntegerField()  # Clave 'a' usada para descifrar
    clave_b = models.IntegerField()  # Clave 'b' usada para descifrar
    mensaje_descifrado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - Descifrado Afin - {self.fecha_creacion}"
