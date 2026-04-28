import sqlite3

DB = "noticias.db"

def crear_base_datos():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS noticias ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "titulo TEXT NOT NULL,"
        "fuente TEXT,"
        "categoria TEXT,"
        "fecha TEXT,"
        "url TEXT,"
        "imagen TEXT,"
        "prioridad INTEGER DEFAULT 0,"
        "UNIQUE(titulo))"
    )
    try:
        cursor.execute("ALTER TABLE noticias ADD COLUMN imagen TEXT")
    except:
        pass
    conn.commit()
    conn.close()
    print("Base de datos lista.")

def guardar_noticias(noticias_dict):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    guardadas = 0
    for categoria, lista in noticias_dict.items():
        for n in lista:
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO noticias "
                    "(titulo, fuente, categoria, fecha, url, imagen, prioridad) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (n["titulo"], n["fuente"], n["categoria"],
                     n["fecha"], n["url"], n.get("imagen", ""), n["prioridad"])
                )
                if cursor.rowcount > 0:
                    guardadas += 1
                elif n.get("imagen", "").startswith("http"):
                    # Noticia ya existía pero sin imagen — actualizarla
                    cursor.execute(
                        "UPDATE noticias SET imagen = ? "
                        "WHERE url = ? AND (imagen IS NULL OR imagen = '')",
                        (n["imagen"], n["url"])
                    )
            except Exception as e:
                print("Error:", e)
    conn.commit()
    conn.close()
    print("Guardadas:", guardadas)

def obtener_noticias(categoria=None, limite=50):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    if categoria:
        cursor.execute(
            "SELECT titulo, fuente, categoria, fecha, url, imagen "
            "FROM noticias WHERE categoria=? "
            "ORDER BY prioridad DESC, id DESC LIMIT ?",
            (categoria, limite)
        )
    else:
        cursor.execute(
            "SELECT titulo, fuente, categoria, fecha, url, imagen "
            "FROM noticias "
            "ORDER BY prioridad DESC, id DESC LIMIT ?",
            (limite,)
        )
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def contar_noticias():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, COUNT(*) FROM noticias GROUP BY categoria")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

if __name__ == "__main__":
    crear_base_datos()
    print("Conteo:", contar_noticias())