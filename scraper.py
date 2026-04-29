import feedparser
import json
from datetime import datetime
import urllib3
urllib3.disable_warnings()

PALABRAS_PROHIBIDAS = [
    "asesinato","homicidio","balacera","ejecutado","crimen",
    "secuestro","extorsion","narco","cartel","muerto","cadaver",
    "detenido","preso","desapareci","sustraccion","abuso sexual",
    "feminicid","violacion","tortur","golpean","rafaguean",
    "presunto","imputado","meme","youtuber","influencer",
]

TEMAS_IMG = {
    "nahle":"https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800",
    "gobernadora":"https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800",
    "alcalde":"https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800",
    "pedro miguel":"https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800",
    "obra":"https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800",
    "carretera":"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800",
    "salud":"https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
    "hospital":"https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800",
    "educacion":"https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800",
    "deporte":"https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
    "futbol":"https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "turismo":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "playa":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "economia":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
    "cultura":"https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800",
    "clima":"https://images.unsplash.com/photo-1504608524841-42584120d693?w=800",
    "agua":"https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
    "empleo":"https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800",
    "inauguracion":"https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800",
    "bienestar":"https://images.unsplash.com/photo-1542596594-649edbc13630?w=800",
    "puerto":"https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800",
}

IMG_CAT = {
    "coatzacoalcos":"https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800",
    "veracruz":"https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    "nacional":"https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800",
}

FUENTES = [
    # Coatzacoalcos
    {"rss":"https://forocoatza.com/feed/","cat":"coatzacoalcos","nombre":"Foro Coatza"},
    {"rss":"https://diariodelistmo.com/feed/","cat":"coatzacoalcos","nombre":"Diario del Istmo"},
    {"rss":"https://liberal.com.mx/feed/","cat":"coatzacoalcos","nombre":"Liberal Coatza"},
    {"rss":"https://municipiosur.com/feed/","cat":"coatzacoalcos","nombre":"Municipio Sur"},
    {"rss":"https://www.alcalorpolitico.com/rss.xml","cat":"coatzacoalcos","nombre":"Al Calor Coatza"},
    # Veracruz
    {"rss":"https://jornadaveracruz.com.mx/feed/","cat":"veracruz","nombre":"Jornada Veracruz"},
    {"rss":"https://lasillarota.com/feed/","cat":"veracruz","nombre":"La Silla Rota"},
    {"rss":"https://golpepolitico.com/feed/","cat":"veracruz","nombre":"Golpe Politico"},
    {"rss":"https://www.veracruznews.mx/feed/","cat":"veracruz","nombre":"Veracruz News"},
    {"rss":"https://www.liberal.com.mx/feed/","cat":"veracruz","nombre":"Liberal del Sur"},
    # Nacional
    {"rss":"https://www.eluniversal.com.mx/rss.xml","cat":"nacional","nombre":"El Universal"},
    {"rss":"https://www.milenio.com/rss","cat":"nacional","nombre":"Milenio"},
    {"rss":"https://www.excelsior.com.mx/rss.xml","cat":"nacional","nombre":"Excelsior"},
]

def es_permitido(titulo):
    t = titulo.lower()
    return not any(p in t for p in PALABRAS_PROHIBIDAS)

def calcular_prioridad(titulo):
    t = titulo.lower()
    if any(p in t for p in ["nahle","gobernadora","rocio"]):
        return 3
    if any(p in t for p in ["alcalde","pedro miguel","coatzacoalcos","ayuntamiento"]):
        return 2
    return 1

def fallback_img(titulo, categoria):
    t = titulo.lower()
    for tema, url in TEMAS_IMG.items():
        if tema in t:
            return url
    return IMG_CAT.get(categoria, IMG_CAT["nacional"])

def extraer_imagen_entry(entry):
    # 1. media_content
    if hasattr(entry, "media_content") and entry.media_content:
        for m in entry.media_content:
            url = m.get("url","")
            if url.startswith("http") and any(
                ext in url.lower() for ext in [".jpg",".jpeg",".png",".webp"]
            ):
                return url
    # 2. media_thumbnail
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        url = entry.media_thumbnail[0].get("url","")
        if url.startswith("http"):
            return url
    # 3. enclosure
    if hasattr(entry, "enclosures") and entry.enclosures:
        for enc in entry.enclosures:
            if "image" in enc.get("type",""):
                return enc.get("href","")
    # 4. summary con img tag
    summary = getattr(entry, "summary", "") or ""
    if "<img" in summary:
        import re
        m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
        if m:
            url = m.group(1)
            if url.startswith("http"):
                return url
    return None

def scrape_fuente(fuente):
    print(f"RSS: {fuente['nombre']}...")
    try:
        import requests
        try:
            resp = requests.get(fuente["rss"], timeout=6, 
                              headers={"User-Agent":"Mozilla/5.0"})
            feed = feedparser.parse(resp.text)
        except Exception as e:
            print(f"  Sin acceso: {e}")
            return []
        if not feed.entries:
            print(f"  Sin entradas")
            return []
        
        noticias = []
        for entry in feed.entries[:15]:
            titulo = entry.get("title","").strip()
            if not titulo or len(titulo) < 20:
                continue
            if not es_permitido(titulo):
                continue
            
            url_nota = entry.get("link", fuente["rss"])
            imagen = extraer_imagen_entry(entry)
            if not imagen:
                imagen = fallback_img(titulo, fuente["cat"])
            
            noticias.append({
                "titulo": titulo[:120],
                "fuente": fuente["nombre"],
                "categoria": fuente["cat"],
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "url": url_nota,
                "imagen": imagen,
                "prioridad": calcular_prioridad(titulo),
            })
        
        print(f"  {len(noticias)} noticias")
        return noticias
    except Exception as e:
        print(f"  Error: {e}")
        return []

def scrape_todas():
    print("Bot iniciando via RSS...")
    coatza, veracruz, nacional = [], [], []
    
    for f in FUENTES:
        noticias = scrape_fuente(f)
        if f["cat"] == "coatzacoalcos":
            coatza += noticias
        elif f["cat"] == "veracruz":
            veracruz += noticias
        else:
            nacional += noticias
    
    # Deduplicar y ordenar
    def dedup_sort(lista):
        vistos = set()
        res = []
        for n in lista:
            if n["titulo"] not in vistos:
                vistos.add(n["titulo"])
                res.append(n)
        res.sort(key=lambda x: x["prioridad"], reverse=True)
        return res
    
    coatza   = dedup_sort(coatza)
    veracruz = dedup_sort(veracruz)
    nacional = dedup_sort(nacional)
    
    print(f"Coatzacoalcos: {len(coatza)}")
    print(f"Veracruz: {len(veracruz)}")
    print(f"Nacional: {len(nacional)}")
    
    return {"coatzacoalcos": coatza, "veracruz": veracruz, "nacional": nacional}

if __name__ == "__main__":
    resultado = scrape_todas()
    with open("noticias.json","w",encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print("Guardado en noticias.json")