from vector_store import model, index, stored_data
import numpy as np

# 🔥 NEW IMPORTS
from news_fetcher import get_stock_news
from vector_store import add_news  
def retrieve(query):
    print("Index size:", index.ntotal)
    print("Stored data size:", len(stored_data))

    # 🔥 STEP 1: Fetch & add news
    news_list = get_stock_news(query)
    add_news(news_list, query)

    if index.ntotal == 0:
        return stored_data[:3]

    query_embedding = model.encode(query)
    query_embedding = np.array([query_embedding])

    D, I = index.search(query_embedding, k=3)

    results = []
    for i in I[0]:
        if i < len(stored_data):
            results.append(stored_data[i])

    if not results:
        return stored_data[:3]

    print("QUERY:", query)
    print("RESULTS:", results)

    return results
