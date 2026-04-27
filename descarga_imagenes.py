import sqlite3
import os
import random
import urllib3
urllib3.disable_warnings()

STATIC_DIR = "static/img"
os.makedirs(STATIC_DIR, exist_ok=True)

RESPALDO = {
    "coatzacoalcos": [
        "https://images.unsplash.com/photo-1588392382834-a891154bca4d?w=800&q=80",
        "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=800&q=80",
        "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80",
        "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
        "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&q=80",
    ],
    "veracruz": [
        "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=800&q=80",
        "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    ],
    "nacional": [
        "https://images.unsplash.com/photo-1569025743873-ea3a9ade89f9?w=800&q=80",
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80",
        "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=80",
    ]
}

def descargar_imagen(url, nombre_archivo):
    ruta = os.path.join(STATIC_DIR, nombre_archivo)
    if os.path.exists(ruta):
        return "/static/img/" + nombre_archivo
    try:
        from curl_cffi import requests
        r = requests.get(url, impersonate="chrome124", timeout=10, verify=False)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(ruta, "wb") as f:
                f.write(r.content)
            return "/static/img/" + nombre_archivo
    except:
        pass
    return None

def procesar_imagenes():
    conn = sqlite3.connect("noticias.db")
    cursor = conn.cursor()
    noticias = cursor.execute(
        "SELECT id, imagen, categoria FROM noticias ORDER BY id DESC LIMIT 200"
    ).fetchall()
    print("Procesando", len(noticias), "noticias...")
    for id, imagen, categoria in noticias:
        nombre = "img_" + str(id) + ".jpg"
        ruta_local = "/static/img/" + nombre
        if os.path.exists(STATIC_DIR + "/" + nombre):
            if imagen != ruta_local:
                cursor.execute("UPDATE noticias SET imagen=? WHERE id=?", (ruta_local, id))
            continue
        url_a_descargar = imagen if imagen and imagen.startswith("http") else None
        if not url_a_descargar:
            url_a_descargar = random.choice(RESPALDO.get(categoria, RESPALDO["nacional"]))
        resultado = descargar_imagen(url_a_descargar, nombre)
        if resultado:
            cursor.execute("UPDATE noticias SET imagen=? WHERE id=?", (resultado, id))
            print("OK:", id, resultado)
        else:
            respaldo = random.choice(RESPALDO.get(categoria, RESPALDO["nacional"]))
            resultado2 = descargar_imagen(respaldo, nombre)
            if resultado2:
                cursor.execute("UPDATE noticias SET imagen=? WHERE id=?", (resultado2, id))
    conn.commit()
    conn.close()
    print("LISTO")

if __name__ == "__main__":
    procesar_imagenes()