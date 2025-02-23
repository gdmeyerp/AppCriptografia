from django.db import models
from django.contrib.auth.models import User

class ArchivoFirmado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo_original = models.FileField(upload_to="archivos_originales/")
    archivo_firmado = models.FileField(upload_to="archivos_firmados/", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)