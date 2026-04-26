from flask import Flask, render_template
from database import crear_base_datos, obtener_noticias, guardar_noticias
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os

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
    if principal:
        principal = list(principal)
        if not principal[5] or not str(principal[5]).startswith("http"):
            from imagenes import obtener_imagen_por_categoria
            principal[5] = obtener_imagen_por_categoria("coatzacoalcos", principal[0])
        principal = tuple(principal)
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
    return "Noticias actualizadas correctamente."

@app.route("/delfines")
def delfines():
    from delfines import obtener_resultado_delfines, obtener_proximo_juego
    resultado = obtener_resultado_delfines()
    proximo = obtener_proximo_juego()
    return render_template("delfines.html", resultado=resultado, proximo=proximo)

if __name__ == "__main__":
    crear_base_datos()
    actualizar_noticias()
    scheduler = BackgroundScheduler()
    scheduler.add_job(actualizar_noticias, "interval", minutes=45)
    scheduler.start()
    print("Bot activo: actualiza cada 45 minutos.")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
