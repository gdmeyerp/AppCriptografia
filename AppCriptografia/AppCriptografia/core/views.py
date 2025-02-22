from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import HistorialCifrado

@login_required
def historial_view(request):
    """Vista para mostrar el historial de cifrado del usuario"""
    historial = HistorialCifrado.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'core/historial.html', {'historial': historial})

def home_view(request):
    """Página principal que muestra enlaces para iniciar sesión o registrarse"""
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard:index')  # Redirige al dashboard
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('core:login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones
        if not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'core/register.html')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'core/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, 'core/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, 'core/register.html')

        # Crear el usuario
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('core:login')

    return render(request, 'core/register.html')

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})
