import time
import random
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

try:
    from curl_cffi import requests
    USAR_CURL = True
    print("Usando curl_cffi - modo stealth activado")
except:
    import requests
    USAR_CURL = False
    print("Usando requests normal")

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

def pausa_humana():
    tiempo = random.uniform(2.0, 6.0)
    print("Esperando " + str(round(tiempo, 1)) + "s...")
    time.sleep(tiempo)

def obtener_pagina(url, reintentos=3):
    for intento in range(reintentos):
        try:
            pausa_humana()
            if USAR_CURL:
                response = requests.get(
                    url,
                    impersonate="chrome124",
                    timeout=20,
                    verify=False,
                    headers={"Accept-Language": "es-MX,es;q=0.9,en;q=0.8"}
                )
            else:
                session = requests.Session()
                session.headers.update({
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
                    "Connection": "keep-alive",
                })
                response = session.get(url, timeout=20, verify=False)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            elif response.status_code == 403:
                print("  Bloqueado 403, reintento " + str(intento+1))
                time.sleep(random.uniform(5, 10))
            elif response.status_code == 404:
                print("  No encontrado 404")
                return None
            else:
                print("  Error " + str(response.status_code))
        except Exception as e:
            print("  Intento " + str(intento+1) + " fallido: " + str(e))
            time.sleep(random.uniform(3, 7))
    return None