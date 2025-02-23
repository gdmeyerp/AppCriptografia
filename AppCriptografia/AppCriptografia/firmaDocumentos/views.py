import io
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm, UploadTwoFileForm
from .cifrado import sign_doc, validate_sign
from .models import ArchivoFirmado
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Vista principal del módulo Firma de Documentos"""
    return render(request, 'firmaDocumentos/index.html')

@login_required
def upload_file_sign(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['file']
            processed_content = sign_doc(file_obj)

            ArchivoFirmado.objects.create(
                usuario=request.user,
                archivo_original=file_obj,
                archivo_firmado=processed_content,
            )

            # Abrir la firma en modo lectura binaria
            with open(processed_content, "rb") as f:
                file_content = f.read()
            
            # Usamos BytesIO para manejar el contenido en memoria.
            processed_file = io.BytesIO(file_content)
            
            # Configuramos la respuesta para descarga.
            response = HttpResponse(processed_file.getvalue(), content_type='application/sig')
            response['Content-Disposition'] = 'attachment; filename="documento_firmado.sig"'
            return response
    else:
        form = UploadFileForm()
    
    return render(request, 'firmaDocumentos/cifrar.html', {'form': form})

@login_required
def validate_sign_view(request):
    if request.method == 'POST':
        form = UploadTwoFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['file1']
            file_sig = request.FILES['file2']
            isSignLegit = validate_sign(file_obj, file_sig)
            
            if isSignLegit:
                resultado = "La firma ha sido validada y es legítima"
            else:
                resultado = "La firma no es legítima"

            return render(request, "firmaDocumentos/validar.html", {
                "resultado": resultado,
                "form": form
            })
    else:
        form = UploadTwoFileForm()
    
    return render(request, 'firmaDocumentos/validar.html', {'form': form})

@login_required
def historial_firmas_view(request):
    datos = ArchivoFirmado.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'firmaDocumentos/historial.html', {'datos': datos})