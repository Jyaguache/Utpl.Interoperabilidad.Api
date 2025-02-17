from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

#seccion mongo_importar libreria
import pymongo
from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import authenticate

#para agregar seguridad a nuestro api
security = HTTPBasic()

#configuracion de mongodb
cliente = pymongo.MongoClient("mongodb+srv://jyutplinteroperabilidad:TGZqGHBPNDfUoKOl@jimmyy.t3n2rcm.mongodb.net/?retryWrites=true&w=majority")
database = cliente["inventario"]
coleccion = database["productos"]

description = """
Utpl Interoperabilidad API - API Productos de un inventario. 🚀

## Productos

Tu puedes crear un producto.
Tu puedes listar productos.

"""
tags_metadata = [
    {
        "name":"productos",
        "description":"Permite realizar un crud completo de los productos del inventario (listar)"
    }
]

app = FastAPI(
    title="Utpl Interoperabilidad API Tarea Sem-12",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Jimmy Javier Yaguache López",
        "url": "https://github.com/Jyaguache/Utpl.Interoperabilidad.Api.git",
        "email": "jjyaguache1@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata   
)

class Producto (BaseModel):
    id: str
    cod: str
    nombre: str
    tipo: str
    categoria: Optional[str] = None
    

class ProductoEntrada (BaseModel):
    cod: str
    nombre:str
    tipo: str
    categoria: Optional[str] = None
    familia: str

inventarioList = []

@app.post("/producto", response_model=Producto, tags = ["productos"])
@version(1,0)
async def crear_producto(invenT: Producto):
    itemProducto = Producto (id=str(uuid.uuid4()), cod = invenT.cod, nombre = invenT.nombre, tipo = invenT.tipo, categoria = invenT.categoria)
    resultadoBase = coleccion.insert_one(itemProducto.dict())
    return itemProducto

@app.post("/producto", response_model=Producto, tags = ["productos"])
@version(2,0)
async def crear_producto(invenT: ProductoEntrada):
    itemProducto = Producto (id=str(uuid.uuid4()), cod = invenT.cod, nombre = invenT.nombre, tipo = invenT.tipo, categoria = invenT.categoria, familia = invenT.familia)
    resultadoBase = coleccion.insert_one(itemProducto.dict())
    return itemProducto

#Seguridades
@app.get("/producto", response_model=List[Producto], tags = ["productos"])
@version(1, 0)
def get_productos(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/producto/{producto_id}", response_model=Producto, tags = ["productos"])
@version(1,0)
def get_producto():
    itemProducto = list(coleccion.find()) ##devolver toda la informacion de la base de datos.
    return itemProducto

## Agregar busqueda por id.
@app.get("/producto/{producto_id}", response_model=Producto, tags = ["productos"])
@version(1,0)
def obtener_producto(producto_id: str):
    item = coleccion.find_one({"id": producto_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

## Agregar busqueda por cod.    
@app.get("/producto/codigo/{cod_num}", response_model=Producto, tags = ["productos"])
@version(2,0) 
def obtener_cod(cod_num: str):
    item = coleccion.find_one({"cod": cod_num})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/producto/{producto_id}", tags = ["productos"])
@version(1,0)
def eliminar_producto (producto_id: str):
    result = coleccion.delete_one({"id": producto_id})
    if result.deleted_count == 1:
        return {"mensaje": "Producto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Inventario no encontrada")
    producto_eliminado = inventarioList.pop(inventario_id)

@app.get("/")
def read_root():
    return {"Hello": "INTEROPERABILIDAD TAREA SEM12"}

app = VersionedFastAPI(app)
