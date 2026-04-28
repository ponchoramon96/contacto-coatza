from bot_seguro import obtener_pagina
from datetime import datetime
import re

PALABRAS_PROHIBIDAS = [
    "asesinato","homicidio","balacera","tiroteo","ejecutado",
    "crimen","criminal","delincuencia","violencia","violento",
    "ataque","secuestro","extorsion","robo","robaron","asalto",
    "narco","cartel","droga","muerto","muertos","cadaver",
    "escandalo","corrupcion","protesta","manifestacion",
    "critica","critican","rechazo","fracaso","falla","herido",
    "accidente","explosion","detenido","preso","capturado","bala",
    "meme","reality","novela","actor","actriz","cantante",
    "espectaculo","farandula","romance","divorcio","show",
    "derbez","mrbeast","youtuber","influencer","tiktok",
    "desaparece","desaparecido","desaparecen","buscan","localizan",
    "renuncia","renuncio","muere","fallece","lesionado",
    "choque","incendio","demanda","queja","escasez",
    "joven desaparece","menor desaparecido","cuerpo",
    "golpean","asesinan","rafaguean","violan","roban",
    "Nossa","Damos","Atuamos","suporte","mercado","empresa",
    "desapareci","desaparec","busca a su","sustraccion","abuso","sexual",
    "detienen","detiene","cae alcalde","arrestan","aprehenden",
    "presunto","imputado","vinculan","proceso","juicio","condena",
    "desap@","recid0","sustrae","navegar","usar la app","instala la app",
    "abuso sexual","detienen al","presunto abuso","busca a su hija",
    "desap", "recid", "feminicid", "violacion", "secuestr", "tortur"
]

PALABRAS_POSITIVAS = [
    "obra","obras","inauguracion","inaugura","desarrollo",
    "inversion","proyecto","empleo","turismo","cultura",
    "festival","deporte","deportivo","torneo","educacion",
    "salud","crecimiento","avance","logro","beneficio",
    "apoyo","mejora","rehabilitacion","entrega","apertura",
    "nahle","rocio","gobernadora","gobierno","alcalde",
    "pedro","municipal","secretaria","programa","bienestar",
    "coatzacoalcos","veracruz","istmo"
]

TITULOS_INVALIDOS = [
    "periodismo trascendente", "portal de noticias", "liberal del sur –",
    "diario del istmo –", "foro coatza –", "noticias de coatzacoalcos"
]

def titulo_es_valido(titulo):
    t = titulo.lower().strip()
    for invalido in TITULOS_INVALIDOS:
        if t.startswith(invalido) or invalido in t[:50]:
            return False
    if len(titulo) < 20:
        return False
    return True

PREFIJOS_A_LIMPIAR = [
    "Coatzacoalcos", "Veracruz", "Nacional", "Local", "Gobierno",
    "Foro Coatza", "Diario del Istmo", "Liberal del Sur", "Golpe Político"
]

def limpiar_titulo(titulo):
    if not titulo:
        return ""
    titulo = titulo.strip()
    for prefijo in PREFIJOS_A_LIMPIAR:
        if titulo.startswith(prefijo):
            titulo = titulo[len(prefijo):].strip(" –-|:")
    return titulo

URLS_IMAGEN_INVALIDAS = [
    "banner", "publicidad", "vacaciones", "verano", "anuncio",
    "header", "logo", "footer", "sidebar", "google", "avatar",
    "placeholder", "default", "noimage", "no-image"
]

def imagen_es_valida(url_img):
    if not url_img:
        return False
    if len(url_img) < 10: # Añadido para filtrar URLs muy cortas
        return False
    url_lower = url_img.lower()
    for palabra in URLS_IMAGEN_INVALIDAS:
        if palabra in url_lower:
            return False
    if not url_lower.startswith("http"): # Asegurar que sea una URL completa
        return False
    return True

FUENTES_COATZA = [
    {"nombre": "Municipio Sur", "url": "https://municipiosur.com"},
    {"nombre": "Diario del Istmo", "url": "https://diariodelistmo.com/seccion/coatzacoalcos"},
    {"nombre": "Foro Coatza", "url": "https://forocoatza.com"},
    {"nombre": "Liberal Coatza", "url": "https://liberal.com.mx/category/lo-nuestro/"},
    {"nombre": "Al Calor Coatza", "url": "https://www.alcalorpolitico.com/informacion/tag/coatzacoalcos-2"},
    {"nombre": "Milenio Alcalde", "url": "https://www.milenio.com/buscar?q=pedro+miguel+coatzacoalcos"},
    {"nombre": "Universal Coatza", "url": "https://www.eluniversal.com.mx/buscar/?q=coatzacoalcos"},
]

FUENTES_VERACRUZ = [
    {"nombre": "Rocio Nahle", "url": "https://m.facebook.com/rocionahle"},
    {"nombre": "Gobierno Veracruz", "url": "https://www.veracruz.gob.mx/noticias"},
    {"nombre": "Jornada Veracruz", "url": "https://jornadaveracruz.com.mx"},
    {"nombre": "La Silla Rota Ver", "url": "https://lasillarota.com/veracruz/"},
    {"nombre": "Notiver", "url": "https://www.notiver.com"},
    {"nombre": "Golpe Politico", "url": "https://golpepolitico.com"},
    {"nombre": "Al Calor Nahle", "url": "https://www.alcalorpolitico.com/informacion/tag/rocio-nahle"},
    {"nombre": "Al Calor Politico", "url": "https://www.alcalorpolitico.com"},
    {"nombre": "Veracruz News", "url": "https://www.veracruznews.mx"},
    {"nombre": "Liberal del Sur", "url": "https://www.liberal.com.mx"},
]

FUENTES_NACIONAL = [
    {"nombre": "El Universal", "url": "https://www.eluniversal.com.mx"},
    {"nombre": "Milenio", "url": "https://www.milenio.com"},
    {"nombre": "Excelsior", "url": "https://www.excelsior.com.mx"},
]

def es_permitida(titulo):
    t = titulo.lower()
    return not any(p in t for p in PALABRAS_PROHIBIDAS)

def calcular_prioridad(titulo):
    t = titulo.lower()
    if any(p in t for p in ["nahle","rocio nahle","gobernadora"]):
        return 3
    if any(p in t for p in ["alcalde","pedro miguel","coatzacoalcos","ayuntamiento"]):
        return 2
    if any(p in t for p in PALABRAS_POSITIVAS):
        return 1
    return 0

def scrape_fuente(fuente, categoria):
    print("Scrapeando " + fuente["nombre"] + "...")
    soup = obtener_pagina(fuente["url"])
    noticias = []
    if not soup:
        print("  Sin acceso")
        return noticias
    vistos = set()
    og_imagen_portada = ""
    try:
        meta = soup.find("meta", property="og:image")
        if meta and meta.get("content","").startswith("http"):
            og_imagen_portada = meta.get("content")
    except:
        pass
    for tag in ["h1","h2","h3"]:
        for el in soup.find_all(tag):
            titulo = el.get_text(strip=True).split('.')[0][:100] # Limitar longitud antes de limpiar
            titulo = limpiar_titulo(titulo)
            if not titulo_es_valido(titulo): continue
            if es_permitida(titulo) and titulo not in vistos:
                enlace = el.find("a")
                url_nota = fuente["url"]
                if enlace and enlace.get("href"):
                    href = enlace["href"]
                    if href.startswith("http"):
                        url_nota = href
                    elif href.startswith("/"):
                        base = "/".join(fuente["url"].split("/")[:3])
                        url_nota = base + href
                
                # Intentar extraer imagen de la página de la lista
                imagen = extraer_imagen(soup)

                # Si no se encuentra imagen en la página de la lista, intentar en la página del artículo
                if not imagen and url_nota != fuente["url"]:
                    try:
                        soup_articulo = obtener_pagina(url_nota)
                        if soup_articulo:
                            imagen = extraer_imagen(soup_articulo)
                    except Exception as e:
                        print(f"  Error al extraer imagen del artículo {url_nota}: {e}")
                
                # Fallback a la imagen de portada si no se encontró ninguna otra
                if not imagen:
                    imagen = og_imagen_portada if imagen_es_valida(og_imagen_portada) else ""

                vistos.add(titulo)
                noticias.append({
                    "titulo": titulo,
                    "fuente": fuente["nombre"],
                    "categoria": categoria,
                    "fecha": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "url": url_nota,
                    "imagen": imagen,
                    "prioridad": calcular_prioridad(titulo)
                })
    print("  " + str(len(noticias)) + " noticias")
    return noticias

def scrape_facebook_publico(url_pagina, categoria):
    print("Scrapeando Facebook: " + url_pagina)
    noticias = []
    try:
        from curl_cffi import requests
        from bs4 import BeautifulSoup
        url_mobile = url_pagina.replace("www.facebook.com", "m.facebook.com")
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Accept-Language": "es-MX,es;q=0.9",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"
        }
        r = requests.get(url_mobile, impersonate="chrome124", timeout=15, verify=False, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            vistos = set()
            for el in soup.find_all(["p","div","span"]):
                texto = el.get_text(strip=True)
                texto = limpiar_titulo(texto)
                if not titulo_es_valido(texto): continue
                if len(texto) < 300 and es_permitida(texto) and texto not in vistos:
                    img = ""
                    img_tag = el.find_previous("img") or el.find_next("img")
                    if img_tag:
                        src = img_tag.get("src","")
                        if src.startswith("http") and "logo" not in src.lower():
                            img = src
                    vistos.add(texto)
                    noticias.append({
                        "titulo": texto[:100],
                        "fuente": "Facebook Oficial",
                        "categoria": categoria,
                        "fecha": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "url": url_pagina,
                        "imagen": img,
                        "prioridad": 3
                    })
            print("  " + str(len(noticias)) + " posts de Facebook")
    except Exception as e:
        print("  Error Facebook: " + str(e))
    return noticias[:5]

def extraer_imagen(soup, url_base=""):
    # 1. Intentar og:image primero (funciona en Veracruz y Nacional)
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        img_url = og["content"].strip()
        if imagen_es_valida(img_url):
            return img_url

    # 2. Buscar en el artículo principal
    for selector in [
        "article img",
        ".post-thumbnail img",
        ".entry-content img",
        ".td-post-content img",
        ".single-post-content img",
        "figure img",
        ".featured-image img",
        ".wp-post-image",
        "img.attachment-large",
        "img.size-large",
        "img.size-full"
    ]:
        tag = soup.select_one(selector)
        if tag:
            src = tag.get("src") or tag.get("data-src") or tag.get("data-lazy-src")
            if src and imagen_es_valida(src):
                return src

    # 3. Buscar twitter:image como último recurso
    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        img_url = tw["content"].strip()
        if imagen_es_valida(img_url):
            return img_url

    return None  # Sin imagen válida encontrada

def scrape_todas():
    print("Bot Contacto Coatza iniciando...")
    coatza = []
    veracruz = []
    nacional = []
    coatza += scrape_facebook_publico("https://www.facebook.com/PedroMiguelOficial", "coatzacoalcos")
    veracruz += scrape_facebook_publico("https://www.facebook.com/rocionahle", "veracruz")
    veracruz += scrape_facebook_publico("https://www.facebook.com/GobiernoDeVeracruz", "veracruz")
    coatza += scrape_facebook_publico("https://www.facebook.com/delfinescoatzacoalcos", "coatzacoalcos")
    for f in FUENTES_COATZA:
        coatza += scrape_fuente(f, "coatzacoalcos")
    for f in FUENTES_VERACRUZ:
        veracruz += scrape_fuente(f, "veracruz")
    for f in FUENTES_NACIONAL:
        nacional += scrape_fuente(f, "nacional")
    coatza.sort(key=lambda x: x["prioridad"], reverse=True)
    veracruz.sort(key=lambda x: x["prioridad"], reverse=True)
    nacional.sort(key=lambda x: x["prioridad"], reverse=True)
    print("Coatzacoalcos: " + str(len(coatza)))
    print("Veracruz: " + str(len(veracruz)))
    print("Nacional: " + str(len(nacional)))
    return {"coatzacoalcos": coatza, "veracruz": veracruz, "nacional": nacional}

if __name__ == "__main__":
    resultado = scrape_todas()
    from database import crear_base_datos, guardar_noticias
    crear_base_datos()
    guardar_noticias(resultado)