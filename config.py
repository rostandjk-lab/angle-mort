import os

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
HANDLE = os.getenv("HANDLE", "@anglemortai")
MAX_AGE_HOURS = 36  # on ne garde que les actus récentes
PER_FEED = 6  # nombre max d'articles lus par flux
MAX_CANDIDATES = 30  # nombre max d'actus envoyées à Gemini

# Un flux qui ne répond pas est simplement ignoré. Tu peux en ajouter ou en retirer.
FEEDS = [
    ("TechCrunch IA", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge IA", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("MIT Technology Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab"),
    ("VentureBeat IA", "https://venturebeat.com/category/ai/feed/"),
    ("Rest of World", "https://restofworld.org/feed/"),
    ("TechCabal", "https://techcabal.com/feed/"),
    ("Techpoint Africa", "https://techpoint.africa/feed/"),
    ("Disrupt Africa", "https://disrupt-africa.com/feed/"),
    ("Google Actu IA Afrique", "https://news.google.com/rss/search?q=intelligence+artificielle+Afrique&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google Actu IA monde", "https://news.google.com/rss/search?q=AI+regulation+OR+AI+chips+OR+AI+investment+when:1d&hl=en-US&gl=US&ceid=US:en"),
]
