import requests
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment variables")
def get_stock_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={API_KEY}"

    res = requests.get(url)
    data = res.json()

    articles = data.get("articles", [])

    news = []
    for a in articles[:5]:
        text = f"{a['title']} {a['description']}"
        news.append(text)

    return news