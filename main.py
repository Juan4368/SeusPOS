from fastapi import FastAPI
from dotenv import load_dotenv
import os
from config import get_db  # noqa: F401  # Mantener import por compatibilidad
import uvicorn
import webbrowser
import threading
import time
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.data.createTable import create_tables  # noqa: F401
from app.routes import (
    productos_router,
    ingresos_router,
    categorias_contabilidad_router,
    egresos_router,
    cartera_router,
)
from app.cargar_productos import cargar_productos_desde_xml  # noqa: F401

app = FastAPI(
    title="POS API",
    version="1.0.0",
    description="API para gestión de productos con arquitectura limpia en python",
    root_path="/AutoServicioLite",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"mensaje": "API POS en ejecución 🚀"}


def open_chrome():
    time.sleep(1)

    url = "http://127.0.0.1:8000/docs"

    chrome_paths = [
        "C://Program Files//Google//Chrome//Application//chrome.exe",
        "C://Program Files (x86)//Google//Chrome//Application//chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(path))
            webbrowser.get("chrome").open_new(url)
            return

    webbrowser.open_new(url)


if __name__ == "__main__":
    threading.Thread(target=open_chrome).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

env = os.getenv("APP_ENV", "dev")
load_dotenv(dotenv_path=".env")

app.include_router(productos_router.router)
app.include_router(ingresos_router.router)
app.include_router(egresos_router.router)
app.include_router(cartera_router.router)
app.include_router(categorias_contabilidad_router.router)
