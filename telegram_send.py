import html
import os
import requests

API = "https://api.telegram.org/bot{token}/{method}"

def _creds():
    return os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]

def send_text(text):
    token, chat = _creds()
    r = requests.post(
        API.format(token=token, method="sendMessage"),
        json={"chat_id": chat, "text": text[:4000]},
        timeout=30,
    )
    r.raise_for_status()

def send_post(post, png_path, chosen, slot, why):
    token, chat = _creds()
    with open(png_path, "rb") as f:
        r = requests.post(
            API.format(token=token, method="sendPhoto"),
            data={"chat_id": chat, "caption": f"Angle mort · post {slot} · image à joindre"},
            files={"photo": f},
            timeout=60,
        )
        r.raise_for_status()
    text = (
        f"<code>{html.escape(post)}</code>\n\n"
        f"Source : {html.escape(chosen['source'])}\n{html.escape(chosen['link'])}\n\n"
        f"Pourquoi : {html.escape(why)}\n"
        f"Vérifie les faits sur la source avant de publier."
    )
    r = requests.post(
        API.format(token=token, method="sendMessage"),
        json={"chat_id": chat, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
        timeout=30,
    )
    r.raise_for_status()
