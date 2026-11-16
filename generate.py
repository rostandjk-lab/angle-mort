import json
import os
import re
from google import genai
from google.genai import types
from config import MODEL
from prompts import SYSTEM, build_user_prompt

def _parse(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    return json.loads(text)

def _validate(data, n_candidates):
    idx = int(data["choice"])
    if not 0 <= idx < n_candidates:
        raise ValueError("choice hors limites")
    post = str(data["post"]).strip()
    if len(post) > 280:
        raise ValueError(f"post trop long ({len(post)} caractères) : raccourcis-le sous 280")
    if data["type"] not in ("opportunite", "menace", "neutre"):
        raise ValueError("type invalide : opportunite, menace ou neutre")
    card = data["card"]
    for key in ("big", "headline", "angle"):
        if not str(card.get(key, "")).strip():
            raise ValueError(f"card.{key} manquant")
    return {
        "choice": idx,
        "type": data["type"],
        "post": post,
        "card": {k: str(card[k]).strip() for k in ("big", "headline", "angle")},
        "why": str(data.get("why", "")).strip(),
    }

def generate_post(candidates, recent):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM,
        response_mime_type="application/json",
        temperature=1.0,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
        ],
    )
    prompt = build_user_prompt(candidates, recent)
    last_error = None
    for _ in range(3):
        response = client.models.generate_content(model=MODEL, contents=prompt, config=config)
        try:
            return _validate(_parse(response.text), len(candidates))
        except Exception as e:
            last_error = e
            prompt += f"\n\nTa réponse précédente était invalide ({e}). Corrige et renvoie le JSON complet."
    raise RuntimeError(f"Gemini n'a pas renvoyé un résultat valide : {last_error}")
