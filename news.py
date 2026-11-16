import calendar
import html
import re
import time
import feedparser
from config import FEEDS, MAX_AGE_HOURS, MAX_CANDIDATES, PER_FEED

feedparser.USER_AGENT = "Mozilla/5.0 (compatible; AngleMortBot/1.0)"

def clean(text, limit):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[:limit]

def fetch_candidates(used_links):
    now = time.time()
    items, seen = [], set()
    for name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"[flux KO] {name}: {e}")
            continue
        if not feed.entries:
            print(f"[flux vide] {name}")
            continue
        for entry in feed.entries[:PER_FEED]:
            link = entry.get("link")
            if not link or link in used_links or link in seen:
                continue
            ts = entry.get("published_parsed") or entry.get("updated_parsed")
            if ts and (now - calendar.timegm(ts)) > MAX_AGE_HOURS * 3600:
                continue
            seen.add(link)
            items.append({
                "source": name,
                "title": clean(entry.get("title"), 200),
                "summary": clean(entry.get("summary"), 400),
                "link": link,
            })
    return items[:MAX_CANDIDATES]
