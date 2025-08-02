from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrar-estado/', views.registrar_estado, name='registrar_estado'),
    path('historial/', views.historial_emocional, name='historial_emocional'),
    path('canciones/', views.vista_canciones, name='canciones'),  # ← 🎵 Nueva ruta para las tarjetas
    path('', views.index, name='index'),
]
