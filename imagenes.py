import requests
import random
import urllib3
urllib3.disable_warnings()

UNSPLASH_KEYWORDS = {
    "gobierno": "government mexico city",
    "obra": "construction urban mexico",
    "salud": "health hospital mexico",
    "educacion": "education school mexico",
    "deporte": "sport mexico",
    "turismo": "tourism veracruz mexico",
    "economia": "economy business mexico",
    "cultura": "culture mexico festival",
    "seguridad": "police security mexico",
    "medio ambiente": "environment nature mexico",
    "default": "veracruz mexico coatzacoalcos"
}

IMAGENES_COATZA = [
    "https://images.unsplash.com/photo-1588392382834-a891154bca4d?w=800&q=80",
    "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=800&q=80",
    "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
    "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
    "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
    "https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=800&q=80",
    "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?w=800&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
]

IMAGENES_VERACRUZ = [
    "https://images.unsplash.com/photo-1518638150340-f706e86654de?w=800&q=80",
    "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?w=800&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "https://images.unsplash.com/photo-1519451241324-20b4ea2c4220?w=800&q=80",
]

IMAGENES_NACIONAL = [
    "https://images.unsplash.com/photo-1569025743873-ea3a9ade89f9?w=800&q=80",
    "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80",
    "https://images.unsplash.com/photo-1529408686214-b48b8532f72c?w=800&q=80",
    "https://images.unsplash.com/photo-1448932223592-d1fc686e76ea?w=800&q=80",
]

def obtener_og_image(url):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="es-MX"
            )
            page = context.new_page()
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            og = page.evaluate("""() => {
                let m = document.querySelector('meta[property="og:image"]') ||
                        document.querySelector('meta[name="twitter:image"]');
                if (m) return m.getAttribute('content');
                let img = document.querySelector('article img') ||
                          document.querySelector('.post-thumbnail img') ||
                          document.querySelector('figure img') ||
                          document.querySelector('.entry-content img');
                if (img) return img.src;
                return null;
            }""")
            browser.close()
            if og and og.startswith("http"):
                return og
    except Exception as e:
        print("  Playwright error: " + str(e))
    try:
        from curl_cffi import requests as cr
        response = cr.get(url, impersonate="chrome124", timeout=10, verify=False)
    except:
        try:
            response = requests.get(url, timeout=10, verify=False,
                headers={"User-Agent": "Mozilla/5.0 Chrome/124.0.0.0"})
        except:
            return None
    if response.status_code != 200:
        return None
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    for meta in soup.find_all("meta"):
        prop = meta.get("property", "") or meta.get("name", "")
        if prop in ["og:image", "twitter:image"]:
            content = meta.get("content", "")
            if content and content.startswith("http"):
                return content
    return None

def obtener_imagen_por_categoria(categoria, titulo=""):
    titulo_lower = titulo.lower()
    for keyword, _ in UNSPLASH_KEYWORDS.items():
        if keyword in titulo_lower and keyword != "default":
            break
    if categoria == "coatzacoalcos":
        return random.choice(IMAGENES_COATZA)
    elif categoria == "veracruz":
        return random.choice(IMAGENES_VERACRUZ)
    else:
        return random.choice(IMAGENES_NACIONAL)

def obtener_imagen(url_noticia, categoria, titulo=""):
    imagen = obtener_og_image(url_noticia)
    if imagen:
        return imagen
    return obtener_imagen_por_categoria(categoria, titulo)

if __name__ == "__main__":
    test_url = "https://www.forocoatza.com"
    print("Probando extraccion de imagen...")
    img = obtener_imagen(test_url, "coatzacoalcos", "prueba gobierno")
    print("Imagen obtenida: " + str(img))