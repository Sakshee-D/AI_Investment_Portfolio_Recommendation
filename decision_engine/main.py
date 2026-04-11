from fastapi import FastAPI
from api.routes import router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API working"}

app.include_router(router)