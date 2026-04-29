import socket
socket.setdefaulttimeout(5)
import feedparser
import requests
import json
import re
from datetime import datetime

PALABRAS_PROHIBIDAS = ["asesinato","homicidio","balacera","ejecutado","crimen","secuestro","extorsion","narco","cartel","muerto","cadaver","detenido","preso","desapareci","sustraccion","abuso sexual","feminicid","violacion","tortur","golpean","rafaguean","presunto","imputado","meme","youtuber","influencer"]

TEMAS_IMG = {"nahle":"https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800","gobernadora":"https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800","alcalde":"https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800","obra":"https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800","salud":"https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800","educacion":"https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800","deporte":"https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800","futbol":"https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800","turismo":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800","economia":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800","cultura":"https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800","clima":"https://images.unsplash.com/photo-1504608524841-42584120d693?w=800","agua":"https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800","empleo":"https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=800","inauguracion":"https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800","bienestar":"https://images.unsplash.com/photo-1542596594-649edbc13630?w=800","puerto":"https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800"}

IMG_CAT = {"coatzacoalcos":"https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800","veracruz":"https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800","nacional":"https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800"}

FUENTES = [{"rss":"https://forocoatza.com/feed/","cat":"coatzacoalcos","nombre":"Foro Coatza"},{"rss":"https://diariodelistmo.com/feed/","cat":"coatzacoalcos","nombre":"Diario del Istmo"},{"rss":"https://liberal.com.mx/feed/","cat":"coatzacoalcos","nombre":"Liberal Coatza"},{"rss":"https://municipiosur.com/feed/","cat":"coatzacoalcos","nombre":"Municipio Sur"},{"rss":"https://www.alcalorpolitico.com/rss.xml","cat":"coatzacoalcos","nombre":"Al Calor Coatza"},{"rss":"https://jornadaveracruz.com.mx/feed/","cat":"veracruz","nombre":"Jornada Veracruz"},{"rss":"https://lasillarota.com/feed/","cat":"veracruz","nombre":"La Silla Rota"},{"rss":"https://golpepolitico.com/feed/","cat":"veracruz","nombre":"Golpe Politico"},{"rss":"https://www.veracruznews.mx/feed/","cat":"veracruz","nombre":"Veracruz News"},{"rss":"https://www.liberal.com.mx/feed/","cat":"veracruz","nombre":"Liberal del Sur"},{"rss":"https://www.eluniversal.com.mx/rss.xml","cat":"nacional","nombre":"El Universal"},{"rss":"https://www.milenio.com/rss","cat":"nacional","nombre":"Milenio"},{"rss":"https://www.excelsior.com.mx/rss.xml","cat":"nacional","nombre":"Excelsior"}]

def es_permitido(titulo):
    t = titulo.lower()
    return not any(p in t for p in PALABRAS_PROHIBIDAS)

def calcular_prioridad(titulo):
    t = titulo.lower()
    if any(p in t for p in ["nahle","gobernadora","rocio"]): return 3
    if any(p in t for p in ["alcalde","pedro miguel","coatzacoalcos","ayuntamiento"]): return 2
    return 1

def fallback_img(titulo, categoria):
    t = titulo.lower()
    for tema, url in TEMAS_IMG.items():
        if tema in t: return url
    return IMG_CAT.get(categoria, IMG_CAT["nacional"])

def get_img(entry):
    if hasattr(entry, "media_content") and entry.media_content:
        u = entry.media_content[0].get("url", "")
        if u.startswith("http"): return u
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        u = entry.media_thumbnail[0].get("url", "")
        if u.startswith("http"): return u
    s = getattr(entry, "summary", "") or ""
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', s)
    if m and m.group(1).startswith("http"): return m.group(1)
    return None

def scrape_fuente(f):
    print(f"[{f['nombre']}]...", flush=True)
    try:
        r = requests.get(f["rss"], timeout=(4,5), headers={"User-Agent":"Mozilla/5.0"}, verify=False)
        print(f"[{f['nombre']}] status={r.status_code}", flush=True)
        feed = feedparser.parse(r.text)
        out = []
        for e in feed.entries[:15]:
            t = e.get("title","").strip()
            if len(t) < 20 or not es_permitido(t): continue
            img = get_img(e) or fallback_img(t, f["cat"])
            out.append({"titulo":t[:120],"fuente":f["nombre"],"categoria":f["cat"],"fecha":datetime.now().strftime("%Y-%m-%d %H:%M"),"url":e.get("link",f["rss"]),"imagen":img,"prioridad":calcular_prioridad(t)})
        print(f"[{f['nombre']}] {len(out)} noticias", flush=True)
        return out
    except Exception as e:
        print(f"[{f['nombre']}] ERROR: {e}", flush=True)
        return []

def scrape_todas():
    print("=== Bot iniciando ===", flush=True)
    coatza, veracruz, nacional = [], [], []
    for f in FUENTES:
        r = scrape_fuente(f)
        if f["cat"] == "coatzacoalcos": coatza += r
        elif f["cat"] == "veracruz": veracruz += r
        else: nacional += r
    def dedup(lista):
        vistos = set(); res = []
        for n in lista:
            if n["titulo"] not in vistos:
                vistos.add(n["titulo"]); res.append(n)
        return sorted(res, key=lambda x: x["prioridad"], reverse=True)
    resultado = {"coatzacoalcos":dedup(coatza),"veracruz":dedup(veracruz),"nacional":dedup(nacional)}
    print(f"=== C:{len(resultado['coatzacoalcos'])} V:{len(resultado['veracruz'])} N:{len(resultado['nacional'])} ===", flush=True)
    return resultado

if __name__ == "__main__":
    r = scrape_todas()
    with open("noticias.json","w",encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print("Guardado en noticias.json", flush=True)