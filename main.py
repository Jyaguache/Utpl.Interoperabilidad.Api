from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth import authenticate

#seccion mongo importar libreria
import pymongo

import spotipy

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='c8519595485648c3949369793de3e366',
    client_secret='d266e54ea24346a7b278445be87cd400'
))

description = """
Utpl Interoperabilidad API - API Productos de un inventario. 🚀

## Productos

Tu puedes crear un producto.
Tu puedes listar productos.


## Tipos

Usted podrá:

* **Crear tipos de productos** (_not implemented_).
"""

tags_metadata = [
    {
        "name":"productos",
        "description": "Permite realizar un crud completo de un producto (listar)"
    },
    {
        "name":"tipos",
        "description": "Permite realizar un crud completo de tipos de productos"
    },
]

app = FastAPI(
    title="Utpl Interoperabilidad Tarea Sem-12",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Jimmy Yaguache",
        "url": "http://x-force.example.com/contact/",
        "email": "jjyaguache1@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)

class Producto (BaseModel):
    id: int
    nombre: str
    tipo: str
    categoria: Optional[str] = None

productoList = []

@app.post("/productos", response_model=Producto)
def crear_producto(product: Producto):
    productoList.append(product)
    return product

@app.get("/productos", response_model=List[Producto])
def get_productos():
    return productoList

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto (producto_id: int):
    for producto in productoList:
        if producto.id == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no existe")

@app.delete("/productos/{producto_id}")
def eliminar_producto (producto_id: int):
    producto = next((p for p in productoList if p.id == producto_id), None)
    if producto:
        productoList.remove(producto)
        return {"mensaje": "producto eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="producto no encontrada")
  

@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad Tarea SEM7"}
