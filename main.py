import datetime
import json
import os
import sys
import traceback
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from card import render_card
from config import HANDLE
from generate import generate_post
from news import fetch_candidates
from telegram_send import send_post, send_text

HISTORY = Path("history.json")

def load_history():
    if HISTORY.exists():
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    return []

def save_history(history):
    HISTORY.write_text(json.dumps(history[-200:], ensure_ascii=False, indent=2), encoding="utf-8")

def run():
    slot = os.getenv("SLOT", "test")
    history = load_history()
    used = {h["link"] for h in history}
    candidates = fetch_candidates(used)
    if len(candidates) < 3:
        send_text("Angle mort : pas assez d'actus fraîches trouvées pour ce créneau.")
        return
    result = generate_post(candidates, history[-6:])
    chosen = candidates[result["choice"]]
    out = Path("out")
    out.mkdir(exist_ok=True)
    png = out / "card.png"
    render_card(result["card"], result["type"], png, HANDLE)
    send_post(result["post"], png, chosen, slot, result["why"])
    history.append({
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"),
        "link": chosen["link"],
        "title": chosen["title"],
        "type": result["type"],
        "post": result["post"],
    })
    save_history(history)

if __name__ == "__main__":
    try:
        run()
    except Exception:
        err = traceback.format_exc()[-1500:]
        print(err)
        try:
            send_text("Angle mort : erreur\n" + err)
        except Exception:
            pass
        sys.exit(1)
