from django import forms 

class UploadFileForm(forms.Form): 
    file = forms.FileField(label='Selecciona un archivo')

class UploadTwoFileForm(forms.Form): 
    file1 = forms.FileField(label='Selecciona un archivo')
    file2 = forms.FileField(label='Selecciona un archivo firma')