from flask import Flask, render_template
from database import crear_base_datos, obtener_noticias, guardar_noticias
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def actualizar_noticias():
    print("Actualizando noticias...")
    import scraper
    resultado = scraper.scrape_todas()
    guardar_noticias(resultado)
    print("Listo.")

@app.route("/")
def index():
    coatza = obtener_noticias("coatzacoalcos", 30)
    veracruz = obtener_noticias("veracruz", 15)
    nacional = obtener_noticias("nacional", 5)
    principal = coatza[0] if coatza else None
    resto = coatza[1:15] if len(coatza) > 1 else []
    if principal and (not principal[5] or not principal[5].startswith("http")):
        from imagenes import obtener_og_image, obtener_imagen_por_categoria
        img = obtener_og_image(principal[4])
        if not img:
            img = obtener_imagen_por_categoria("coatzacoalcos", principal[0])
        principal = list(principal)
        principal[5] = img
        principal = tuple(principal)
    fecha = datetime.now().strftime("%a %d %b %Y").upper()
    return render_template("index.html",
        principal=principal,
        resto=resto,
        veracruz=veracruz,
        nacional=nacional,
        fecha=fecha
    )

if __name__ == "__main__":
    crear_base_datos()
    scheduler = BackgroundScheduler()
    scheduler.add_job(actualizar_noticias, "interval", minutes=45)
    scheduler.start()
    print("Bot activo: actualiza cada 6 horas.")
    app.run(debug=False)
