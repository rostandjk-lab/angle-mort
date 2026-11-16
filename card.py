import html
from pathlib import Path
from playwright.sync_api import sync_playwright

ACCENTS = {
    "opportunite": ("#F5B83D", "OPPORTUNITÉ"),
    "menace": ("#FF5A4D", "MENACE"),
    "neutre": ("#5CC8FF", "À RETENIR"),
}

def big_size(text):
    n = len(text)
    if n <= 5:
        return 240
    if n <= 8:
        return 190
    if n <= 12:
        return 140
    return 100

def render_card(card, kind, out_path, handle):
    accent, kicker = ACCENTS.get(kind, ACCENTS["neutre"])
    big = card["big"][:14]
    template = (Path(__file__).parent / "templates" / "card.html").read_text(encoding="utf-8")
    replacements = {
        "ACCENT": accent,
        "KICKER": kicker,
        "BIG": html.escape(big),
        "BIGSIZE": str(big_size(big)),
        "HEADLINE": html.escape(card["headline"][:100]),
        "ANGLE": html.escape(card["angle"][:120]),
        "HANDLE": html.escape(handle),
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
