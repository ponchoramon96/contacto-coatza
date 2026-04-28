import urllib3
import random
urllib3.disable_warnings()

TEMAS = {
    "nahle": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
    "gobernadora": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
    "alcalde": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
    "pedro miguel": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",
    "obra": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80",
    "carretera": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80",
    "salud": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80",
    "hospital": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80",
    "educacion": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80",
    "escuela": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80",
    "deporte": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=80",
    "futbol": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&q=80",
    "turismo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    "playa": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    "economia": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
    "inversion": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
    "cultura": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80",
    "festival": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80",
    "seguridad": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80",
    "policia": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80",
    "medio ambiente": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80",
    "agua": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
    "empleo": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80",
    "trabajo": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800&q=80",
    "vivienda": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&q=80",
    "bienestar": "https://images.unsplash.com/photo-1542596594-649edbc13630?w=800&q=80",
    "programa": "https://images.unsplash.com/photo-1542596594-649edbc13630?w=800&q=80",
    "apertura": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800&q=80",
    "inauguracion": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800&q=80",
    "puerto": "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800&q=80",
    "coatzacoalcos": "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800&q=80",
}

IMAGENES_CATEGORIA = {
    "coatzacoalcos": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Coatzacoalcos_mexico.jpg/1280px-Coatzacoalcos_mexico.jpg",
    "veracruz": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Veracruz_malecon.jpg/1280px-Veracruz_malecon.jpg",
    "nacional": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Mexico_City_Zocalo.jpg/1280px-Mexico_City_Zocalo.jpg",
    "delfines": "https://upload.wikimedia.org/wikipedia/commons/5/52/Delfines_coatzacoalcos.jpg"
}

def imagen_por_titulo(titulo, categoria):
    t = titulo.lower()
    for tema, url in TEMAS.items():
        if tema in t:
            return url
    return IMAGENES_CATEGORIA.get(categoria, IMAGENES_CATEGORIA["coatzacoalcos"])

def obtener_imagen_por_categoria(categoria, titulo=""):
    return imagen_por_titulo(titulo, categoria)

def obtener_og_image(url):
    return None

def obtener_imagen(url, categoria, titulo=""):
    return imagen_por_titulo(titulo, categoria)