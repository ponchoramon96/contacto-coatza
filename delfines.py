import requests
import urllib3
urllib3.disable_warnings()

def obtener_resultado_delfines():
    try:
        url = "https://www.sofascore.com/api/v1/team/1071790/events/last/0"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.sofascore.com"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            eventos = data.get("events", [])
            if eventos:
                ultimo = eventos[-1]
                local = ultimo["homeTeam"]["name"]
                visitante = ultimo["awayTeam"]["name"]
                goles_local = ultimo.get("homeScore", {}).get("current", "-")
                goles_visitante = ultimo.get("awayScore", {}).get("current", "-")
                estado = ultimo.get("status", {}).get("description", "")
                return {
                    "local": local,
                    "visitante": visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "estado": estado
                }
    except Exception as e:
        print("Error Delfines: " + str(e))
    return None

def obtener_proximo_juego():
    try:
        url = "https://www.sofascore.com/api/v1/team/1071790/events/next/0"
        headers = {
            "User-Agent": "Mozilla/5.0 Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.sofascore.com"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            eventos = data.get("events", [])
            if eventos:
                proximo = eventos[0]
                local = proximo["homeTeam"]["name"]
                visitante = proximo["awayTeam"]["name"]
                from datetime import datetime
                timestamp = proximo.get("startTimestamp", 0)
                fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
                return {"local": local, "visitante": visitante, "fecha": fecha}
    except Exception as e:
        print("Error proximo juego: " + str(e))
    return None

if __name__ == "__main__":
    r = obtener_resultado_delfines()
    print("Ultimo resultado:", r)
    p = obtener_proximo_juego()
    print("Proximo juego:", p)