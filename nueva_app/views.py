from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'nueva_app/index.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'nueva_app/registro.html', {'error': 'Las contraseñas no coinciden.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'nueva_app/registro.html', {'error': 'El usuario ya existe.'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')

    return render(request, 'nueva_app/registro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')  # Redirige a perfil tras login exitoso
        else:
            context = {'error': 'Usuario o contraseña incorrectos'}
            return render(request, 'nueva_app/login.html', context)

    else:
        return render(request, 'nueva_app/login.html')

@login_required
def perfil(request):
    return render(request, 'nueva_app/perfil.html', {'usuario': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
