from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ImagenCifradaAES, ImagenDescifradaAES
from .cifrado import cifrar_imagen_aes, descifrar_imagen_aes
from django.http import HttpResponse
from .forms import ImageAESUploadForm, CipheredImageAESUploadForm # Import a form to handle file upload
import os
from django.conf import settings

@login_required
def index(request):
    """Vista principal del módulo de cifrado AES"""
    return render(request, 'aes/index.html')


def vista_cifrar_aes(request):
    original_image_url = None
    encrypted_image_url = None
    applied_aes_key = None

    # If the form was submitted (POST request)
    if request.method == 'POST':
        encrypt_image_form = ImageAESUploadForm(request.POST, request.FILES)
        if encrypt_image_form.is_valid():
            original_image_instance = encrypt_image_form.save(commit=False)
            original_image_instance.usuario = request.user
            applied_aes_key = encrypt_image_form.cleaned_data['clave']

            if len(applied_aes_key) != 8:
                return render(request, 'aes/cifrar.html', {
                    'encrypt_image_form': encrypt_image_form, 'error': "La clave debe tener 16, 24 o 32 caracteres."
                })
            
            original_image_instance.clave = applied_aes_key
            original_image_instance.save()

            original_image_url = original_image_instance.image.url # Store original image URL

            # Encrypt
            original_image_path = os.path.join(settings.MEDIA_ROOT, original_image_instance.image.name)
            encrypted_image_filename = f"encrypted_aes_{original_image_instance.image.name.split('/')[-1]}"
            encrypted_image_save_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/cifradas', encrypted_image_filename)

            cifrar_imagen_aes(original_image_path, encrypted_image_save_path, applied_aes_key)
            encrypted_image_url = f"/media/imagenes/cifradas/{encrypted_image_filename}" # Store encrypted image URL

            ImagenCifradaAES.objects.create(usuario=request.user, image=f"imagenes/cifradas/{encrypted_image_filename}")

            return render(request, 'aes/cifrar.html', {
                'original_image_url': original_image_url,
                'encrypted_image_url': encrypted_image_url,
                'applied_aes_key': applied_aes_key
            })
        
    return render(request, 'aes/cifrar.html', {'encrypt_image_form': ImageAESUploadForm()})
    


def vista_descifrar_aes(request):
    original_encrypted_image_url = None
    decrypted_image_url = None
    applied_aes_key = None

    # If the form was submitted (POST request)
    if request.method == 'POST':
        decrypt_image_form = CipheredImageAESUploadForm(request.POST, request.FILES)
        if decrypt_image_form.is_valid():
            original_encrypted_image_instance = decrypt_image_form.save(commit=False)
            original_encrypted_image_instance.usuario = request.user
            applied_aes_key = decrypt_image_form.cleaned_data['clave']

            if len(applied_aes_key) != 8:
                return render(request, 'aes/descifrar.html', {
                    'decrypt_image_form': decrypt_image_form, 'error': "La clave debe tener 16, 24 o 32 caracteres."
                })
            
            original_encrypted_image_instance.clave = applied_aes_key
            original_encrypted_image_instance.save()

            original_encrypted_image_url = original_encrypted_image_instance.image.url # Store original image URL

            # Decrypt
            original_encrypted_image_path = os.path.join(settings.MEDIA_ROOT, original_encrypted_image_instance.image.name)
            decrypted_image_filename = f"decrypted_aes_{original_encrypted_image_instance.image.name.split('/')[-1]}"
            decrypted_image_save_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/descifradas', decrypted_image_filename)

            descifrar_imagen_aes(original_encrypted_image_path, decrypted_image_save_path, applied_aes_key)
            decrypted_image_url = f"/media/imagenes/descifradas/{decrypted_image_filename}" # Store decrypted image URL

            ImagenDescifradaAES.objects.create(usuario=request.user, image=f"imagenes/descifradas/{decrypted_image_filename}")

            return render(request, 'aes/descifrar.html', {
                'original_encrypted_image_url': original_encrypted_image_url,
                'decrypted_image_url': decrypted_image_url,
                'applied_aes_key': applied_aes_key
            })
        
    return render(request, 'aes/descifrar.html', {'decrypt_image_form': CipheredImageAESUploadForm()})
    


@login_required
def gallery(request):
    """Vista de todas las imagenes subidas y sus encriptaciones"""
    uploaded_original_images = ImagenCifradaAES.objects.filter(usuario=request.user)
    uploaded_encrypted_images = ImagenDescifradaAES.objects.filter(usuario=request.user)
    

    return render(request, 'aes/gallery.html', {
        'uploaded_original_images': uploaded_original_images,
        'uploaded_encrypted_images': uploaded_encrypted_images
    })