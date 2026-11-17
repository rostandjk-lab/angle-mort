import html
from pathlib import Path
from playwright.sync_api import sync_playwright
from illustrations import get_pixel_illustration

ACCENTS = {
    "opportunite": ("#F5B83D", "OPPORTUNITÉ", "LEVIER: RAPIDE", "rocket"),
    "menace": ("#FF5A4D", "MENACE CRITIQUE", "SIGNAL: DANGER", "server_alert"),
    "neutre": ("#5CC8FF", "ANGLE MORT TECH", "RADAR: ACTIF", "radar_eye"),
}

def big_size(text):
    n = len(text)
    if n <= 5:
        return 105
    if n <= 8:
        return 88
    if n <= 12:
        return 72
    return 58

def render_card(card, kind, out_path, handle):
    accent, kicker, default_tag, default_icon = ACCENTS.get(kind, ACCENTS["neutre"])
    big = card["big"][:14]
    
    # Détection intelligente du sujet pour choisir la bonne illustration pixel art
    text_corpus = (card.get("headline", "") + " " + card.get("angle", "") + " " + big).lower()
    if any(k in text_corpus for k in ("puce", "chip", "nvidia", "gpu", "hardware", "modèle", "llm")):
        icon_type = "ai_chip"
        tag = "HARDWARE: IA"
    elif any(k in text_corpus for k in ("panne", "crash", "panique", "coupure", "serveur", "cloud", "microsoft", "aws")):
        icon_type = "server_alert"
        tag = "INFRA: DANGER"
    elif kind == "opportunite" or any(k in text_corpus for k in ("lancer", "vite", "open source", "gratuit", "code")):
        icon_type = "rocket"
        tag = "OPPORTUNITÉ"
    else:
        icon_type = default_icon
        tag = default_tag

    svg_illustration = get_pixel_illustration(kind=icon_type, accent=accent)

    template = (Path(__file__).parent / "templates" / "card.html").read_text(encoding="utf-8")
    replacements = {
        "ACCENT": accent,
        "KICKER": kicker,
        "BIG": html.escape(big),
        "BIGSIZE": str(big_size(big)),
        "HEADLINE": html.escape(card["headline"][:95]),
        "ANGLE": html.escape(card["angle"][:130]),
        "HANDLE": html.escape(handle),
        "HANDLE_RAW": html.escape(handle.lstrip("@")),
        "ILLUSTRATION": svg_illustration,
        "ILLUS_TAG": tag,
    }
    for key, value in replacements.items():
        template = template.replace(f"[[{key}]]", value)
        
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=2)
        page.set_content(template, wait_until="networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        page.screenshot(path=str(out_path))
        browser.close()
