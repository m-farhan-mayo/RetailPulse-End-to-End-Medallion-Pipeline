from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

from app.routers import revenue
from app.routers import products
from app.routers import stores

app = FastAPI(
    title="RetailPulse API",
    version="1.0"
)

# ---------------- ROUTERS ---------------- #

app.include_router(revenue.router)
app.include_router(products.router)
app.include_router(stores.router)

# ---------------- ROOT ---------------- #

@app.get("/", response_class=HTMLResponse)

def root():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------- HEALTH ---------------- #

@app.get("/health")

def health():

    return {
        "status": "healthy"
    }