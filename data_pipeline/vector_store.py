from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from stock_data import get_stock_data

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.IndexFlatL2(384)
stored_data = []

def add_to_index(data):
    global stored_data

    # -------- SAFE DEFAULTS --------
    for key in ["marketCap", "pe", "revenueGrowth", "debtToEquity", "dividendYield", "beta"]:
        if data.get(key) is None:
            data[key] = 0

    # -------- IMPROVED LOGIC --------

    # Size
    size = "large cap" if data["marketCap"] > 500000000000 else "mid/small cap"

    # Risk
    if data["beta"] < 1 and data["debtToEquity"] < 100:
        risk = "low risk"
    else:
        risk = "higher risk"

    # Valuation
    if data["pe"] < 15:
        valuation = "undervalued"
    elif data["pe"] > 30:
        valuation = "overvalued"
    else:
        valuation = "fairly valued"

    # Growth
    growth = "high growth" if data["revenueGrowth"] > 0.1 else "moderate growth"

    # Dividend
    dividend = "good dividend" if data["dividendYield"] > 0.02 else "low dividend"

    # -------- FINAL SUMMARY --------
    summary = f"{data['stock']} is a {size} stock in {data['sector']} sector. It is {valuation} with PE {data['pe']}. The company shows {growth} and has {risk}. It offers {dividend}. Suitable for {'long term investment' if size == 'large cap' else 'short to medium term investment'}."

    # -------- USE SUMMARY --------
    embedding = model.encode([summary])
    index.add(np.array(embedding))

    stored_data.append({
        **data,
        "summary": summary
    })

def add_news(news_list, query):
    global stored_data

    for n in news_list:
        summary = f"News about {query}: {n}"

        embedding = model.encode([summary])
        index.add(np.array(embedding))

        stored_data.append({
            "type": "news",
            "stock": query,
            "summary": summary
        })
        
# -------- BUILD INDEX --------
if index.ntotal == 0:
    data_list = get_stock_data()
    for item in data_list:
        add_to_index(item)

print("Index built:", index.ntotal)