from django.db import models

class HistorialIC(models.Model):
    texto = models.TextField()
    metodo = models.CharField(max_length=50)
    longitud_clave = models.IntegerField()
    ic = models.FloatField()
    similitud = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Texto: {self.texto[:20]}... | Longitud Clave: {self.longitud_clave} | IC: {self.ic}"
