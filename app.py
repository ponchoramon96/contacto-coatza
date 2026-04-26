from flask import Flask, render_template
from database import crear_base_datos, obtener_noticias, guardar_noticias
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os
import random

app = Flask(__name__)

IMAGENES_RESPALDO = {
    "coatzacoalcos": [
        "https://images.unsplash.com/photo-1588392382834-a891154bca4d?w=800&q=80",
        "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=800&q=80",
        "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
        "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
        "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
    ],
    "veracruz": [
        "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=800&q=80",
        "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?w=800&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    ],
    "nacional": [
        "https://images.unsplash.com/photo-1569025743873-ea3a9ade89f9?w=800&q=80",
        "https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=800&q=80",
        "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
    ]
}

def imagen_valida(img):
    return img and str(img).startswith("http") and len(str(img)) > 10

def asignar_imagen(noticia):
    n = list(noticia)
    if not imagen_valida(n[5]):
        n[5] = random.choice(IMAGENES_RESPALDO.get(n[2], IMAGENES_RESPALDO["nacional"]))
    return tuple(n)

def actualizar_noticias():
    print("Actualizando noticias...")
    try:
        import scraper
        resultado = scraper.scrape_todas()
        guardar_noticias(resultado)
        print("Noticias actualizadas.")
    except Exception as e:
        print("Error actualizando:", e)

@app.route("/")
def index():
    coatza = obtener_noticias("coatzacoalcos", 30)
    veracruz = obtener_noticias("veracruz", 15)
    nacional = obtener_noticias("nacional", 5)
    coatza = [asignar_imagen(n) for n in coatza]
    veracruz = [asignar_imagen(n) for n in veracruz]
    nacional = [asignar_imagen(n) for n in nacional]
    principal = coatza[0] if coatza else None
    resto = coatza[1:15] if len(coatza) > 1 else []
    fecha = datetime.now().strftime("%a %d %b %Y").upper()
    return render_template("index.html",
        principal=principal,
        resto=resto,
        veracruz=veracruz,
        nacional=nacional,
        fecha=fecha
    )

@app.route("/actualizar")
def actualizar_manual():
    actualizar_noticias()
    return "OK"

crear_base_datos()
actualizar_noticias()
scheduler = BackgroundScheduler()
scheduler.add_job(actualizar_noticias, "interval", minutes=45)
scheduler.start()
print("Bot activo: actualiza cada 45 minutos.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
