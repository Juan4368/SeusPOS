# 📖 Manual Técnico de Librerías Externas

Este documento describe en detalle las librerías externas utilizadas en el proyecto, 
sus casos de uso, ejemplos de implementación y buenas prácticas.

---

## 📑 Índice
1. [FastAPI](#fastapi)
2. [Starlette](#starlette)
3. [Uvicorn](#uvicorn)
4. [Mangum](#mangum)
5. [SQLAlchemy](#sqlalchemy)
6. [Psycopg2 / Psycopg2-binary](#psycopg2--psycopg2-binary)
7. [Pandas](#pandas)
8. [Numpy](#numpy)
9. [Openpyxl + et_xmlfile](#openpyxl--et_xmlfile)
10. [Python-dotenv / dotenv](#python-dotenv--dotenv)
11. [Pydantic / Pydantic-settings](#pydantic--pydantic-settings)
12. [Python-dateutil](#python-dateutil)
13. [Pytz + Tzdata](#pytz--tzdata)
14. [Click](#click)
15. [Colorama](#colorama)
16. [Anyio + Sniffio](#anyio--sniffio)

---

## FastAPI
**Versión:** 0.115.12  
**Descripción:** Framework moderno para construir **APIs basadas en ASGI**.  
**Casos de uso:**
- Backend de un POS para exponer APIs de productos, ventas, clientes.  
- APIs para integrarse con WhatsApp o sistemas de facturación electrónica.  
**Ejemplo:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/productos/{id}")
def obtener_producto(id: int):
    return {"id": id, "nombre": "Arroz", "precio": 2500}
```

---

## Starlette
**Versión:** 0.46.1  
**Descripción:** Framework **ASGI ligero** sobre el que está construido FastAPI.  
**Casos de uso:**  
- Middleware personalizado (seguridad, logging, CORS).  
- Endpoints simples si no necesitas toda la potencia de FastAPI.  

---

## Uvicorn
**Versión:** 0.34.0  
**Descripción:** Servidor **ASGI ultrarrápido** basado en `uvloop` y `httptools`.  
**Casos de uso:**  
- Correr aplicaciones FastAPI o Starlette en desarrollo y producción.  
**Ejemplo (terminal):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Mangum
**Versión:** 0.19.0  
**Descripción:** Adaptador para ejecutar apps **ASGI en AWS Lambda**.  
**Casos de uso:**  
- Desplegar un FastAPI en AWS Lambda sin tener que montar EC2.  
**Ejemplo:**
```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Hola Lambda"}

handler = Mangum(app)
```

---

## SQLAlchemy
**Versión:** 1.4.54  
**Descripción:** ORM completo para modelar datos en Python y conectarlos a bases SQL.  
**Casos de uso:**  
- Manejar inventarios en PostgreSQL con modelos de producto, stock, ventas.  
**Ejemplo:**
```python
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

engine = create_engine("sqlite:///tienda.db")
metadata = MetaData()

productos = Table(
    "productos", metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String),
    Column("precio", Integer),
)

metadata.create_all(engine)
```

---

## Psycopg2 / Psycopg2-binary
**Versión:** 2.9.10  
**Descripción:** Driver **PostgreSQL** para Python.  
**Casos de uso:**  
- Conectar FastAPI o scripts de carga (Excel → BD).  
**Ejemplo:**
```python
import psycopg2

conn = psycopg2.connect("dbname=tienda user=postgres password=secret")
cur = conn.cursor()
cur.execute("SELECT * FROM productos;")
print(cur.fetchall())
```

---

## Pandas
**Versión:** 2.3.2  
**Descripción:** Librería para análisis y manipulación de datos.  
**Casos de uso:**  
- Importar inventario desde Excel y cargarlo a PostgreSQL.  
- Generar reportes de ventas diarias, márgenes, etc.  
**Ejemplo:**
```python
import pandas as pd

df = pd.read_excel("inventario.xlsx")
print(df.head())

df.to_csv("inventario.csv", index=False)
```

---

## Numpy
**Versión:** 2.3.2  
**Descripción:** Base matemática para cálculos numéricos y arreglos multidimensionales.  
**Casos de uso:**  
- Estadísticas de ventas.  
- Operaciones rápidas sobre precios y cantidades.  
**Ejemplo:**
```python
import numpy as np

ventas = np.array([1000, 1500, 2000])
print("Promedio:", ventas.mean())
```

---

## Openpyxl + et_xmlfile
**Versión:** 3.1.5 / 2.0.0  
**Descripción:** Manejo de archivos Excel (`.xlsx`).  
**Casos de uso:**  
- Importar listas de productos de proveedores.  
- Exportar reportes de ventas a Excel.  
**Ejemplo:**
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws["A1"] = "Producto"
ws["B1"] = "Precio"
ws.append(["Arroz", 2500])
wb.save("productos.xlsx")
```

---

## Python-dotenv / dotenv
**Versión:** 1.1.0 / 0.9.9  
**Descripción:** Maneja **variables de entorno** desde un archivo `.env`.  
**Casos de uso:**  
- Guardar credenciales de BD y tokens sin exponerlos en código.  
**Ejemplo:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv("DATABASE_URL"))
```

---

## Pydantic / Pydantic-settings
**Versión:** 2.11.2 / 2.8.1  
**Descripción:** Validación de datos y manejo de configuración basado en clases.  
**Casos de uso:**  
- Validar productos recibidos por API.  
- Manejar settings con `.env`.  
**Ejemplo:**
```python
from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float

p = Producto(nombre="Arroz", precio=2000)
print(p)
```

---

## Python-dateutil
**Versión:** 2.9.0.post0  
**Descripción:** Manejo flexible de fechas y parsing natural.  
**Casos de uso:**  
- Leer fechas de archivos de proveedores en distintos formatos.  
**Ejemplo:**
```python
from dateutil.parser import parse

fecha = parse("15/08/2025 10:00")
print(fecha)
```

---

## Pytz + Tzdata
**Versión:** 2025.2  
**Descripción:** Soporte de **zonas horarias**.  
**Casos de uso:**  
- Guardar fechas en UTC y mostrar en hora local (ej: Bogotá).  
**Ejemplo:**
```python
from datetime import datetime
import pytz

zona = pytz.timezone("America/Bogota")
print(datetime.now(zona))
```

---

## Click
**Versión:** 8.1.8  
**Descripción:** Framework para construir **CLI (Command Line Interfaces)**.  
**Casos de uso:**  
- Script para cargar inventario desde Excel con un comando.  
**Ejemplo:**
```python
import click

@click.command()
@click.option("--archivo", help="Ruta del Excel")
def cargar(archivo):
    click.echo(f"Cargando inventario desde {archivo}")

if __name__ == "__main__":
    cargar()
```

---

## Colorama
**Versión:** 0.4.6  
**Descripción:** Colorear salidas de consola (útil para logs).  
**Casos de uso:**  
- Mostrar alertas o errores en color rojo al correr scripts.  
**Ejemplo:**
```python
from colorama import Fore, Style

print(Fore.RED + "Error crítico" + Style.RESET_ALL)
```

---

## Anyio + Sniffio
**Versión:** 4.9.0 / 1.3.1  
**Descripción:** Librerías para **manejo de asincronía** en Python.  
- `anyio`: interfaz unificada para asyncio, trio, curio.  
- `sniffio`: detecta qué loop asincrónico se está usando.  
**Casos de uso:**  
- Tareas paralelas (ej: consulta simultánea a APIs de inventario y precios).  
**Ejemplo:**
```python
import anyio

async def tarea():
    print("Hola desde async")

anyio.run(tarea)
```

---
