from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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
