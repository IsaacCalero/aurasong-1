from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nueva_app.urls')),  # Aquí incluyes las urls de tu app
]
