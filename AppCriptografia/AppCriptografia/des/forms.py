from django import forms
from .models import ImagenCifradaDES, ImagenDescifradaDES


class ImageDESUploadForm(forms.ModelForm):
    use_raster = forms.BooleanField(
        required=False,
        label="Cifrar pixeles en vez de archivo"
        )  # A checkbox (True/False)
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
    use_raster = forms.BooleanField(
        required=False,
        label="Cifrar pixeles en vez de archivo"
        )  # A checkbox (True/False)
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