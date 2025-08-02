from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import EstadoEmocional, Cancion
from django.http import JsonResponse
from nueva_app.services.importador_deezer import DeezerImportador

def importar_musica(request):
    artista = request.GET.get('artista', '')
    if not artista:
        return JsonResponse({'error': 'Debe proporcionar un nombre de artista.'}, status=400)

    importador = DeezerImportador(artista)
    cantidad = importador.importar()
    return JsonResponse({'mensaje': f'Se importaron {cantidad} canciones de {artista}.'})


# Página principal
def index(request):
    return render(request, 'nueva_app/index.html')


# Registro de usuario (usando modelo User)
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

        # Crear el usuario con el sistema de Django
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        return redirect('login')

    return render(request, 'nueva_app/registro.html')


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            return render(request, 'nueva_app/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'nueva_app/login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Vista del perfil emocional
@login_required
def perfil(request):
    usuario = request.user
    estado = EstadoEmocional.objects.filter(usuario__username=usuario.username).last()
    cancion = None
    if estado:
        cancion = Cancion.objects.filter(sentimiento_asociado=estado.deseado).first()

    context = {
        'usuario': usuario,
        'estado': estado,
        'cancion': cancion,
    }
    return render(request, 'nueva_app/perfil.html', context)


# Registrar cómo se siente el usuario
@login_required
def registrar_estado(request):
    if request.method == 'POST':
        actual = request.POST.get('estado_actual')
        deseado = request.POST.get('estado_deseado')
        EstadoEmocional.objects.create(
            usuario=request.user,
            actual=actual,
            deseado=deseado
        )
        return redirect('perfil')

    return render(request, 'nueva_app/registrar_estado.html')


# Mostrar todas las canciones asociadas al estado deseado
@login_required
def canciones_por_estado(request):
    estado = EstadoEmocional.objects.filter(usuario__username=request.user.username).last()
    canciones = []
    if estado:
        canciones = Cancion.objects.filter(sentimiento_asociado=estado.deseado)

    return render(request, 'nueva_app/canciones.html', {
        'estado': estado,
        'canciones': canciones
    })


# Historial emocional del usuario
@login_required
def historial_emocional(request):
    historial = EstadoEmocional.objects.filter(usuario__username=request.user.username).order_by('-fecha')
    return render(request, 'nueva_app/historial.html', {'historial': historial})

def vista_canciones(request):
    canciones = Cancion.objects.all().order_by('-id')
    return render(request, 'nueva_app/canciones.html', {'canciones': canciones})
