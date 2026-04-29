import socket
socket.setdefaulttimeout(5)

import feedparser
import requests
import json
import re
from datetime import datetime

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
    "carretera":"https://images.unsplash.com/photo-14648227590    "carretera":"https://images.unsplash.com/photo-1464822sh.com/photo-1576091160550-2173dba999ef?w=800",
    "hospital":"https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800",
    "educacion":"https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800",
    "deporte":"https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
    "futbol":"https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800",
    "turismo":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    "economia":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
    "cultura":"https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800",
    "clima":"https://images.unsplash.com/photo-1504608524841-42584120d693?w=800",
    "agua":"https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800",
    "empleo":"https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800",
    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "inaugurac"h    "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "in      "inauguracion":    "inauguracion":    "inauguracion":    "inauguracion":    "ina0",
    "veracruz":"https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    "nacional":"https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800",
}

FUENTES = [
    {"rss":"https://forocoatza.com/feed/","cat":"coatzacoalcos","nombre":"Foro Coatza"},
    {"rss":"https://diariodelistmo.com/feed/","cat":"coatzacoalcos","nombre":"Diario del Istmo"},
    {"rss":"https://liberal.com.mx/feed/","cat":"coatzacoalcos","nombre":"Liberal Coatza"},
    {"rss":"https://municipiosur.com/feed/","cat":"coatzacoalcos","nombre":"Municipio Sur"},
    {"rss":"https://www.alcalorpolitico.com/rss.xml","cat":"coatzacoalcos","nombre":"Al Calor Coatza"},
    {"rss":"https://jornadaveracruz.com.mx/feed/","cat":"veracruz","nombre":"Jornada Veracruz"},
    {"rss":"https://lasillarota.com/feed/","cat":"veracruz","nombre":"La Silla Rota"},
    {"rss":"https://golpepolitico.com/feed/","cat":"veracruz","nombre":"Golpe Politico"},
    {"rss":"https://www.veracruznews.mx/feed/","cat":"veracruz","nombre":"Veracruz News"},
    {"rss":"https://www.liberal.com.mx/feed/","cat":"veracruz","nombre":"Liberal del Sur"},
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
    if hasattr(entry, "media_content") and entry.media_content:
        for m in entry.media_content:
            url = m.get("url","")
            if url.startswith("http"):
                return url
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        url = entry.media_thumbnail[0].get("url","")
        if url.st        if url.st        if url.st        if url.st        if url.st        if url.st   ""
                       y:
               search(r'<img[^>]+src=["\']([^"\']+)["\']', summary)
        if m and m.group(1).startswith("http")        if m and mrn m.        if m and m.group(1).startswith("http")        if mrin        if m anom        if m and m.group(1).startswith("http")        if m and mrn m.        if m andfu        if m a           timeout=(4, 5),
            headers={"User-Agent":"Mozilla/5.0"},
            verify=False
        )
                         'nombre']}] status {resp.                         'nombre']}] status {resp. r.par                         'nombr=                          'nombre']}] status {resp.            = entry.get("title","").strip()
                                         <                                                                                                           <                   magen =                                         <         , fuente["cat"])
            noticias.append({
                "titulo": titulo[:120],
                "fuente": fuente["nombre"],
                "categoria": fuente["cat"],
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "url": url_nota,
                "imagen": imagen,
                "prioridad": calcular_prioridad(titulo),
            })
        print(f"[{fuente['nombre']}] {len(noticias)} noticias", flush=True)
        return notici        return notici        return notici      fu        return noticOR: {        sh=True)
        return []

def scrape_todas():
    print("=== Bot iniciando ===", flush=True)
    coatza, veracruz, nacional = [], [], []
    for f in FUENTES:
        r = scrape_fuente(f)
        if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatzacoalcos": coatz        if f["catur        if f["cat"] == "cox["p        if f["cat"] == "coatzacoalcos= {        if f["cat"] == "coatzacoalcos": coed        if f["cat"] == "coatzacoalcos": co          if f["cat"] == "coatzacoalcos": coatz        if f["cat"] =['        if f["cat"] == "coatz'nac        if f["cat"] == "coat    re        if f["cat"] == "coatzacoalcos": coatz        ifto        if fth         if f["cat"] == "coatzacoalcos": coatz        if f["cat"] == "coatznsure_ascii=False, indent=2)
    print("Guardado en noticias.json", flush=True)
