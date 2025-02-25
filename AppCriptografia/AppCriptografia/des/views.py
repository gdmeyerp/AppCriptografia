from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ImagenCifradaDES, ImagenDescifradaDES
from .cifrado import cifrar_imagen_des, descifrar_imagen_des
from django.http import HttpResponse
from .forms import ImageDESUploadForm, CipheredImageDESUploadForm # Import a form to handle file upload
import os
from django.conf import settings

@login_required
def index(request):
    """Vista principal del módulo de cifrado DES"""
    return render(request, 'des/index.html')


def vista_cifrar_des(request):
    original_image_url = None
    encrypted_image_url = None
    applied_des_key = None

    # If the form was submitted (POST request)
    if request.method == 'POST':
        encrypt_image_form = ImageDESUploadForm(request.POST, request.FILES)
        if encrypt_image_form.is_valid():
            original_image_instance = encrypt_image_form.save(commit=False)
            original_image_instance.usuario = request.user
            applied_des_key = encrypt_image_form.cleaned_data['clave']

            if len(applied_des_key) != 8:
                return render(request, 'des/cifrar.html', {
                    'encrypt_image_form': encrypt_image_form, 'error': "La clave debe tener exactamente 8 caracteres."
                })
            
            original_image_instance.clave = applied_des_key
            original_image_instance.save()

            original_image_url = original_image_instance.imagen_original.url # Store original image URL

            # Encrypt
            original_image_path = os.path.join(settings.MEDIA_ROOT, original_image_instance.imagen_original.name)
            encrypted_image_filename = f"encrypted_des_{original_image_instance.imagen_original.name.split('/')[-1]}"
            encrypted_image_save_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/cifradas', encrypted_image_filename)

            cifrar_imagen_des(original_image_path, encrypted_image_save_path, applied_des_key)
            encrypted_image_url = f"/media/imagenes/cifradas/{encrypted_image_filename}" # Store encrypted image URL

            ImagenCifradaDES.objects.create(usuario=request.user, imagen_original=f"imagenes/cifradas/{encrypted_image_filename}")

            return render(request, 'des/cifrar.html', {
                'original_image_url': original_image_url,
                'encrypted_image_url': encrypted_image_url,
                'applied_des_key': applied_des_key
            })
        
    return render(request, 'des/cifrar.html', {'encrypt_image_form': ImageDESUploadForm()})
    


def vista_descifrar_des(request):
    original_encrypted_image_url = None
    decrypted_image_url = None
    applied_des_key = None

    # If the form was submitted (POST request)
    if request.method == 'POST':
        decrypt_image_form = CipheredImageDESUploadForm(request.POST, request.FILES)
        if decrypt_image_form.is_valid():
            original_encrypted_image_instance = decrypt_image_form.save(commit=False)
            original_encrypted_image_instance.usuario = request.user
            applied_des_key = decrypt_image_form.cleaned_data['clave']

            if len(applied_des_key) != 8:
                return render(request, 'des/descifrar.html', {
                    'decrypt_image_form': decrypt_image_form, 'error': "La clave debe tener exactamente 8 caracteres."
                })
            
            original_encrypted_image_instance.clave = applied_des_key
            original_encrypted_image_instance.save()

            original_encrypted_image_url = original_encrypted_image_instance.image.url # Store original image URL

            # Decrypt
            original_encrypted_image_path = os.path.join(settings.MEDIA_ROOT, original_encrypted_image_instance.image.name)
            decrypted_image_filename = f"decrypted_des_{original_encrypted_image_instance.image.name.split('/')[-1]}"
            decrypted_image_save_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/descifradas', decrypted_image_filename)

            descifrar_imagen_des(original_encrypted_image_path, decrypted_image_save_path, applied_des_key)
            decrypted_image_url = f"/media/imagenes/descifradas/{decrypted_image_filename}" # Store decrypted image URL

            ImagenDescifradaDES.objects.create(usuario=request.user, image=f"imagenes/descifradas/{decrypted_image_filename}")

            return render(request, 'des/descifrar.html', {
                'original_encrypted_image_url': original_encrypted_image_url,
                'decrypted_image_url': decrypted_image_url,
                'applied_des_key': applied_des_key
            })
        
    return render(request, 'des/descifrar.html', {'decrypt_image_form': CipheredImageDESUploadForm()})
    


@login_required
def gallery(request):
    """Vista de todas las imagenes subidas y sus encriptaciones"""
    uploaded_original_images = ImagenCifradaDES.objects.filter(usuario=request.user)
    uploaded_encrypted_images = ImagenDescifradaDES.objects.filter(usuario=request.user)
    

    return render(request, 'des/gallery.html', {
        'uploaded_original_images': uploaded_original_images,
        'uploaded_encrypted_images': uploaded_encrypted_images
    })