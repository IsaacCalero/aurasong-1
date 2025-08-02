import requests
from nueva_app.models import Cancion

class DeezerImportador:
    BASE_URL = "https://api.deezer.com/search?q=artist:'{artista}'"
    
    # Límites definidos por el modelo Django y validados en la base de datos
    MAX_TITULO = 500
    MAX_ARTISTA = 300
    MAX_URL = 500

    def __init__(self, artista):
        self.artista = artista.strip()
        self.resultados = []

    def buscar_canciones(self):
        try:
            url = self.BASE_URL.format(artista=self.artista)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.resultados = response.json().get("data", [])
        except (requests.RequestException, ValueError) as e:
            print(f"⚠️ Error al buscar canciones: {e}")
            self.resultados = []

    def guardar_en_bd(self, limite=None):
        nuevas = 0
        canciones_a_guardar = self.resultados[:limite] if limite else self.resultados

        for item in canciones_a_guardar:
            try:
                titulo_original = item.get("title", "")
                artista_original = item.get("artist", {}).get("name", "")
                preview_original = item.get("preview", "")

                if not titulo_original or not artista_original:
                    continue  # Saltamos si faltan datos esenciales

                # Recorte inteligente
                titulo = titulo_original[:self.MAX_TITULO]
                artista_nombre = artista_original[:self.MAX_ARTISTA]
                preview = preview_original[:self.MAX_URL]

                # Mensajes informativos si hubo truncamiento
                if len(titulo_original) > self.MAX_TITULO:
                    print(f"✂️ Título recortado: '{titulo_original}' → '{titulo}'")

                if len(artista_original) > self.MAX_ARTISTA:
                    print(f"✂️ Artista recortado: '{artista_original}' → '{artista_nombre}'")

                if len(preview_original) > self.MAX_URL:
                    print(f"✂️ Preview recortado: '{preview_original[:60]}...'")

                # Evita duplicados
                if not Cancion.objects.filter(titulo=titulo, artista=artista_nombre).exists():
                    Cancion.objects.create(
                        titulo=titulo,
                        artista=artista_nombre,
                        url_preview=preview,
                    )
                    nuevas += 1

            except Exception as e:
                print(f"⚠️ Error al guardar canción '{titulo_original}': {e}")
                continue  # No interrumpe todo el proceso si una canción falla

        return nuevas

    def importar(self, cantidad_maxima=None):
        self.buscar_canciones()

        if not self.resultados:
            print("🚫 No se encontraron canciones o hubo un problema con la API.")
            return 0

        return self.guardar_en_bd(cantidad_maxima)
