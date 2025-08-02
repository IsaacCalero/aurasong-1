from django.db import models
from django.contrib.auth.models import User

# Guarda cómo se siente el usuario actualmente y cómo desea sentirse.
class EstadoEmocional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actual = models.CharField(max_length=50)
    deseado = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.actual} → {self.deseado})"

# Contiene canciones relacionadas con estados emocionales específicos.
class Cancion(models.Model):
    titulo = models.CharField(max_length=500)  # antes 200
    artista = models.CharField(max_length=300)  # o más
    url_preview = models.URLField(max_length=500, blank=True, null=True)




    def __str__(self):
        return self.titulo

# Almacena entradas generales: símbolos, pensamientos o gestos.
class Entrada(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Registra interacciones o eventos que involucran a un usuario.
class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    referencia = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.referencia}"

# Documentos que recopilan contenido emocional, narrativo o técnico.
class Documento(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Configuraciones del sistema que pueden influir en el comportamiento emocional o técnico.
class Configuracion(models.Model):
    clave = models.CharField(max_length=50, unique=True)
    valor = models.TextField()

    def __str__(self):
        return self.clave

# Parámetros que regulan intensidad, sensibilidad u otros valores emocionales.
class Parametro(models.Model):
    nombre = models.CharField(max_length=50)
    valor_numerico = models.FloatField()
    valor_textual = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Representa el paso simbólico entre una Entrada inicial y una final — como una transición emocional.
class Proceso(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    salida = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name="procesos_salida")
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.entrada} → {self.salida}"

# Archivos cargados o generados: imágenes, sonidos, documentos simbólicos.
class Archivo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    ruta = models.FileField(upload_to='archivos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Elemento genérico que puede representar un gesto, color, símbolo u objeto visual.
class Elemento(models.Model):
    etiqueta = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    valor = models.TextField()

    def __str__(self):
        return self.etiqueta
