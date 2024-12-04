from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Vista para registro de usuarios
def registro_usuario(request):
    if request.method == "POST":
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario)
            return redirect('perfil')
    else:
        formulario = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'formulario': formulario})

# Vista para iniciar sesión
def iniciar_sesion(request):
    if request.method == "POST":
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            nombre_usuario = formulario.cleaned_data.get('username')
            contrasena = formulario.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect('perfil')
    else:
        formulario = AuthenticationForm()
    return render(request, 'usuarios/iniciar_sesion.html', {'formulario': formulario})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')

# Vista para perfil de usuario
@login_required
def perfil_usuario(request):
    perfil = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})
