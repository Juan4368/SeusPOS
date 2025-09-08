# Documentación de Librerías del Proyecto

Este documento resume las librerías usadas en el proyecto, su propósito principal y ejemplos básicos de uso.

---

## annotated-types (v0.7.0)
**Descripción:**  
Extiende `typing` en Python permitiendo anotaciones más precisas en tipos.  
Se utiliza junto con Pydantic para validaciones.

**Ejemplo:**
```python
from annotated_types import Ge
from typing import Annotated

PositiveInt = Annotated[int, Ge(0)]
```

---

## anyio (v4.9.0)
**Descripción:**  
Librería de concurrencia que unifica `asyncio`, `trio` y `curio`.  
Es usada internamente por FastAPI y Starlette.

**Ejemplo:**
```python
import anyio

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(print, "Hola AnyIO!")

anyio.run(main)
```

---

## click (v8.1.8)
**Descripción:**  
Framework para construir interfaces de línea de comandos (CLI).

**Ejemplo:**
```python
import click

@click.command()
@click.option("--name", prompt="Tu nombre")
def hello(name):
    click.echo(f"Hola {name}!")

if __name__ == "__main__":
    hello()
```

---

## colorama (v0.4.6)
**Descripción:**  
Agrega colores al texto en terminales Windows/Linux.

**Ejemplo:**
```python
from colorama import Fore, Style

print(Fore.RED + "Texto en rojo" + Style.RESET_ALL)
```

---

## config (v0.5.1)
**Descripción:**  
Permite manejar configuraciones de manera sencilla usando archivos `.py` o `.json`.

**Ejemplo:**
```python
import config

cfg = config.Config({"db": "postgres"})
print(cfg.db)
```

---

## dotenv (v0.9.9) / python-dotenv (v1.1.0)
**Descripción:**  
Maneja variables de entorno desde un archivo `.env`.

**Ejemplo:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("DATABASE_URL"))
```

---

## et_xmlfile (v2.0.0)
**Descripción:**  
Dependencia usada por `openpyxl` para escritura eficiente de XML en archivos Excel.

---

## fastapi (v0.115.12)
**Descripción:**  
Framework moderno, rápido y basado en `async` para crear APIs.

**Ejemplo:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hola FastAPI"}
```

---

## greenlet (v3.1.1)
**Descripción:**  
Proporciona corrutinas ligeras que SQLAlchemy usa para operaciones asíncronas.

---

## h11 (v0.14.0)
**Descripción:**  
Implementación pura de HTTP/1.1 en Python. Usada por Uvicorn/Starlette.

---

## idna (v3.10)
**Descripción:**  
Soporte para nombres de dominio internacionalizados.

---

## mangum (v0.19.0)
**Descripción:**  
Adaptador para ejecutar aplicaciones ASGI (como FastAPI) en AWS Lambda.

---

## numpy (v2.3.2)
**Descripción:**  
Librería fundamental para cálculos numéricos y arreglos multidimensionales.

**Ejemplo:**
```python
import numpy as np

a = np.array([1,2,3])
print(a.mean())
```

---

## openpyxl (v3.1.5)
**Descripción:**  
Lectura y escritura de archivos Excel (`.xlsx`).

**Ejemplo:**
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws["A1"] = "Hola Excel"
wb.save("ejemplo.xlsx")
```

---

## pandas (v2.3.2)
**Descripción:**  
Manipulación y análisis de datos en estructuras tipo DataFrame.

**Ejemplo:**
```python
import pandas as pd

df = pd.DataFrame({"producto": ["A", "B"], "precio": [100, 200]})
print(df.head())
```

---

## psycopg2 (v2.9.10)
**Descripción:**  
Driver PostgreSQL para Python.  
**psycopg2-binary** es la versión empaquetada lista para usar.

**Ejemplo:**
```python
import psycopg2

conn = psycopg2.connect("dbname=test user=postgres password=secret")
cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
```

---

## pydantic (v2.11.2) + pydantic-settings
**Descripción:**  
Validación de datos y configuración basada en clases.  
Muy usado en FastAPI.

**Ejemplo:**
```python
from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float

p = Producto(nombre="Arroz", precio=2500)
print(p)
```

---

## python-dateutil (v2.9.0.post0)
**Descripción:**  
Extiende `datetime` para manejo avanzado de fechas.

**Ejemplo:**
```python
from dateutil.parser import parse

fecha = parse("2025-01-01 10:00:00")
print(fecha)
```

---

## pytz / tzdata (v2025.2)
**Descripción:**  
Soporte de zonas horarias.

**Ejemplo:**
```python
from datetime import datetime
import pytz

zona = pytz.timezone("America/Bogota")
print(datetime.now(zona))
```

---

## six (v1.17.0)
**Descripción:**  
Compatibilidad entre Python 2 y 3.

---

## sniffio (v1.3.1)
**Descripción:**  
Detecta qué librería de async se está usando (`asyncio`, `trio`, etc.).

---

## SQLAlchemy (v1.4.54)
**Descripción:**  
ORM para interactuar con bases de datos SQL (PostgreSQL, MySQL, etc.).

**Ejemplo:**
```python
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

engine = create_engine("sqlite:///:memory:")
metadata = MetaData()

usuarios = Table(
    "usuarios", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String),
)

metadata.create_all(engine)
```

---

## starlette (v0.46.1)
**Descripción:**  
Framework ASGI ligero sobre el cual está construido FastAPI.

---

## typing-inspection / typing-extensions
**Descripción:**  
Soporte extendido para anotaciones de tipos en Python.

---

## uvicorn (v0.34.0)
**Descripción:**  
Servidor ASGI ultrarrápido para correr aplicaciones FastAPI/Starlette.

**Ejemplo:**
```bash
uvicorn main:app --reload
```
