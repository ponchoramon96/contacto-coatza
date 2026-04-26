import random
import urllib3
urllib3.disable_warnings()

IMAGENES_TEMAS = {
    "gobernadora": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
    "alcalde": "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
    "obra": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80",
    "salud": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80",
    "educacion": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80",
    "deporte": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=80",
    "turismo": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    "economia": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
    "cultura": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80",
    "seguridad": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80",
}

IMAGENES_COATZA = [
    "https://images.unsplash.com/photo-1588392382834-a891154bca4d?w=800&q=80",
    "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=800&q=80",
    "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
    "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
    "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
]

IMAGENES_VERACRUZ = [
    "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=800&q=80",
    "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?w=800&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "https://images.unsplash.com/photo-1529419412599-7bb870e11810?w=800&q=80",
]

IMAGENES_NACIONAL = [
    "https://images.unsplash.com/photo-1569025743873-ea3a9ade89f9?w=800&q=80",
    "https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=800&q=80",
    "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
    "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80",
]

def imagen_por_titulo(titulo, categoria):
    t = titulo.lower()
    for tema, url in IMAGENES_TEMAS.items():
        if tema in t:
            return url
    if categoria == "coatzacoalcos":
        return random.choice(IMAGENES_COATZA)
    elif categoria == "veracruz":
        return random.choice(IMAGENES_VERACRUZ)
    return random.choice(IMAGENES_NACIONAL)

def obtener_og_image(url):
    try:
        from curl_cffi import requests as cr
        r = cr.get(url, impersonate="chrome124", timeout=10, verify=False)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, "html.parser")
            for prop in ["og:image","twitter:image"]:
                meta = soup.find("meta", property=prop) or soup.find("meta", attrs={"name":prop})
                if meta and meta.get("content","").startswith("http"):
                    return meta.get("content")
    except:
        pass
    return None

def obtener_imagen(url, categoria, titulo=""):
    img = obtener_og_image(url)
    if img:
        return img
    return imagen_por_titulo(titulo, categoria)

def obtener_imagen_por_categoria(categoria, titulo=""):
    return imagen_por_titulo(titulo, categoria)