from django import forms
from .models import ImagenCifradaDES, ImagenDescifradaDES

class ImageDESUploadForm(forms.ModelForm):
    clave = forms.CharField(
        max_length=8,
        required=True,
        label="Ingresar código de 8 bytes"
        ) 
    class Meta:
        model = ImagenCifradaDES
        fields = ['imagen_original','clave']
        labels = {
            'imagen_original': 'Ingrese una imagen'
        }

class CipheredImageDESUploadForm(forms.ModelForm):
    clave = forms.CharField(
        max_length=8,
        required=True,
        label="Ingresar código de 8 bytes"
        )
    
    class Meta:
        model = ImagenDescifradaDES
        fields = ['imagen_cifrada','clave']
        labels = {
            'imagen_cifrada': 'Ingrese una imagen cifrada'
        }