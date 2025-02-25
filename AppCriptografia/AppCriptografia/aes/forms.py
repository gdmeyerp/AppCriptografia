from django import forms
from .models import ImagenCifradaAES, ImagenDescifradaAES

class ImageAESUploadForm(forms.ModelForm):
    clave = forms.CharField(
        min_length=16,
        max_length=32,
        required=True,
        label="Ingresar código de 16, 24 o 32 bytes"
        ) 
    class Meta:
        model = ImagenCifradaAES
        fields = ['imagen_original','clave']
        labels = {
            'imagen_original': 'Ingrese una imagen'
        }

class CipheredImageAESUploadForm(forms.ModelForm):
    clave = forms.CharField(
        min_length=16,
        max_length=32,
        required=True,
        label="Ingresar código de 16, 24 o 32 bytes"
        )
    class Meta:
        model = ImagenDescifradaAES
        fields = ['imagen_cifrada','clave']
        labels = {
            'imagen_cifrada': 'Ingrese una imagen cifrada'
        }