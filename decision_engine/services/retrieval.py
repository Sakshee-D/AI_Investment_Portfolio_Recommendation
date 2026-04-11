import requests

def get_context(query):
    res = requests.get(
        "http://localhost:8000/retrieve",
        params={"query": query}
    )
    return res.json()