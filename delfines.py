import urllib3
urllib3.disable_warnings()

def obtener_resultado_delfines():
    try:
        from curl_cffi import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Accept-Language": "es-MX,es;q=0.9"
        }
        urls = [
            "https://www.sofascore.com/api/v1/team/1071790/events/last/0",
        ]
        for url in urls:
            try:
                r = requests.get(url, impersonate="chrome124", timeout=10, verify=False,
                    headers={"Accept": "application/json", "Referer": "https://www.sofascore.com"})
                if r.status_code == 200:
                    data = r.json()
                    eventos = data.get("events", [])
                    if eventos:
                        u = eventos[-1]
                        return {
                            "local": u["homeTeam"]["name"],
                            "visitante": u["awayTeam"]["name"],
                            "goles_local": u.get("homeScore", {}).get("current", "-"),
                            "goles_visitante": u.get("awayScore", {}).get("current", "-"),
                            "estado": u.get("status", {}).get("description", "Finalizado")
                        }
            except:
                continue
    except Exception as e:
        print("Error Delfines:", e)
    return {
        "local": "Delfines Coatzacoalcos",
        "visitante": "Próximo rival",
        "goles_local": "-",
        "goles_visitante": "-",
        "estado": "Ver Facebook: /delfinescoatzacoalcos"
    }

def obtener_noticias_delfines():
    noticias = []
    try:
        from curl_cffi import requests
        from bs4 import BeautifulSoup
        urls = [
            "https://www.masnoticias.mx/?s=delfines+coatzacoalcos",
            "https://www.liberal.com.mx/?s=delfines+coatzacoalcos",
            "https://forocoatza.com/?s=delfines",
        ]
        for url in urls:
            try:
                r = requests.get(url, impersonate="chrome124", timeout=12, verify=False)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    for tag in ["h2","h3"]:
                        for el in soup.find_all(tag)[:5]:
                            texto = el.get_text(strip=True)[:100]
                            if len(texto) > 20 and texto not in noticias:
                                noticias.append(texto)
            except:
                continue
    except Exception as e:
        print("Error:", e)
    return noticias[:6]

if __name__ == "__main__":
    print(obtener_resultado_delfines())
    print(obtener_noticias_delfines())