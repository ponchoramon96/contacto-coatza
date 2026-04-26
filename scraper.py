from bot_seguro import obtener_pagina
from datetime import datetime

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
    "desaparece","desaparecido","localizar","Nossa","Damos","Atuamos",
    "suporte","mercado","clientes","empresa"
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
    from imagenes import obtener_imagen
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
                img_tag = el.find_next("img")
                imagen = ""
                if img_tag:
                    imagen = img_tag.get("src") or img_tag.get("data-src") or ""
                    if imagen and imagen.startswith("/"):
                        base = "/".join(fuente["url"].split("/")[:3])
                        imagen = base + imagen
                if not imagen or not imagen.startswith("http"):
                    imagen = obtener_imagen(url_nota, categoria, titulo)
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

def scrape_todas():
    print("Bot Contacto Coatza iniciando...")
    coatza = []
    veracruz = []
    nacional = []
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