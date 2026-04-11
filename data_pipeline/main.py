from fastapi import FastAPI
from retrieve import retrieve

app = FastAPI()

@app.get("/retrieve")
def get_context(query: str):
    
    return retrieve(query)