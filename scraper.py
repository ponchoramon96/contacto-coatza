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
    "abuso sexual","detienen al","presunto abuso","busca a su hija"
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
            titulo = el.get_text(strip=True).split('.')[0][:100]
            if len(titulo) > 25 and es_permitida(titulo) and titulo not in vistos:
                enlace = el.find("a")
                url_nota = fuente["url"]
                if enlace and enlace.get("href"):
                    href = enlace["href"]
                    if href.startswith("http"):
                        url_nota = href
                    elif href.startswith("/"):
                        base = "/".join(fuente["url"].split("/")[:3])
                        url_nota = base + href
                imagen = ""
                try:
                    img_cerca = el.find_previous("img") or el.find_next("img")
                    if img_cerca:
                        src = img_cerca.get("src") or img_cerca.get("data-src") or img_cerca.get("data-lazy-src") or ""
                        if src.startswith("http") and not src.endswith(".svg") and "logo" not in src.lower() and "icon" not in src.lower():
                            imagen = src
                except:
                    pass
                if not imagen and url_nota != fuente["url"]:
                    try:
                        soup_art = obtener_pagina(url_nota)
                        if soup_art:
                            meta_art = soup_art.find("meta", property="og:image") or soup_art.find("meta", attrs={"name":"twitter:image"})
                            if meta_art and meta_art.get("content","").startswith("http"):
                                imagen = meta_art.get("content")
                            if not imagen:
                                for sel in ["article img","figure img",".post img",".entry-content img",".featured img"]:
                                    img_tag = soup_art.select_one(sel)
                                    if img_tag:
                                        src = img_tag.get("src") or img_tag.get("data-src") or ""
                                        if src.startswith("http") and "logo" not in src.lower():
                                            imagen = src
                                            break
                    except:
                        pass
                if not imagen:
                    imagen = og_imagen_portada
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
                if len(texto) > 40 and len(texto) < 300 and es_permitida(texto) and texto not in vistos:
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