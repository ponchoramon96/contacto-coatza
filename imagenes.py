import urllib3
import requests
from bs4 import BeautifulSoup
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
    "clima": "https://images.unsplash.com/photo-1504608524841-42584120d693?w=800&q=80",
    "lluvia": "https://images.unsplash.com/photo-1504608524841-42584120d693?w=800&q=80",
    "calor": "https://images.unsplash.com/photo-1504608524841-42584120d693?w=800&q=80",
}

IMAGENES_CATEGORIA = {
    "coatzacoalcos": "https://images.unsplash.com/photo-1585208798174-6cedd86e019a?w=800&q=80",
    "veracruz": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
    "nacional": "https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800&q=80",
    "gobierno": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
    "delfines": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&q=80",
}

URLS_INVALIDAS = [
    "banner", "publicidad", "vacaciones", "verano", "anuncio",
    "header", "logo", "footer", "sidebar", "google", "avatar",
    "placeholder", "default", "noimage", "no-image", "spinner",
    "loading", "pixel", "tracking", "1x1", "blank"
]

def url_imagen_valida(url):
    if not url or len(url) < 15:
        return False
    if not url.startswith("http"):
        return False
    url_lower = url.lower()
    for palabra in URLS_INVALIDAS:
        if palabra in url_lower:
            return False
    return True

def obtener_og_image(url):
    """Fetches the article URL and extracts the real image."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=8, verify=False)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")

        # 1. og:image
        og = soup.find("meta", property="og:image")
        if og and og.get("content") and url_imagen_valida(og["content"]):
            return og["content"].strip()

        # 2. twitter:image
        tw = soup.find("meta", attrs={"name": "twitter:image"})
        if tw and tw.get("content") and url_imagen_valida(tw["content"]):
            return tw["content"].strip()

        # 3. Imagen dentro del artículo
        for selector in [
            "article img", ".post-thumbnail img", ".entry-content img",
            ".td-post-content img", "figure img", ".featured-image img",
            "img.attachment-large", "img.size-large", "img.size-full",
            ".wp-post-image", ".single-post img"
        ]:
            tag = soup.select_one(selector)
            if tag:
                src = (tag.get("src") or tag.get("data-src") 
                       or tag.get("data-lazy-src") or "")
                if url_imagen_valida(src):
                    return src.strip()

    except Exception as e:
        print(f"[imagenes] Error obteniendo imagen de {url}: {e}")
    return None

def imagen_por_titulo(titulo, categoria):
    t = titulo.lower()
    for tema, url in TEMAS.items():
        if tema in t:
            return url
    return IMAGENES_CATEGORIA.get(
        categoria.lower(), 
        IMAGENES_CATEGORIA["coatzacoalcos"]
    )

def obtener_imagen_por_categoria(categoria, titulo=""):
    return imagen_por_titulo(titulo, categoria)

def obtener_imagen(url, categoria, titulo=""):
    """Intenta obtener imagen real del artículo, si no usa fallback por tema."""
    if url:
        real = obtener_og_image(url)
        if real:
            return real
    return imagen_por_titulo(titulo, categoria)