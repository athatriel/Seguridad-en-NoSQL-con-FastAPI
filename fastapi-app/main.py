from fastapi import FastAPI, Request, HTTPException
from urllib.parse import quote_plus
from pydantic import BaseModel
from pymongo import MongoClient
from slowapi import Limiter
from slowapi.util import get_remote_address
import os, requests
import logging

logging.basicConfig(level=logging.INFO)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="API NoSQL (hardened)")
mongo = MongoClient("mongodb://admin:Iamtheadmin@mongo:27017/tienda")
# mongo = MongoClient(os.getenv("MONGO_HOST","mongo"), 27017)
db = mongo[os.getenv("MONGO_DATABASE","tienda")]

class Login(BaseModel): username: str; password: str
class Pedido(BaseModel): producto: str; cantidad: int

@app.post("/login_mongo")
@limiter.limit("5/minute")
async def login(request: Request, data: Login):

    # ❌ NoSQLi: acepta operadores $ en credenciales
    user = db.usuarios.find_one({"username": data.username,
                                 "password": data.password}, {"_id":0})
    if user: return {"msg":"ok"}
    logging.warning(f"Intento de login fallido para {data.username}")
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/pedidos")
def crear_pedido(pedido: Pedido):

    if not pedido.producto.strip():
        raise HTTPException(status_code=400,detail="El producto es obligatorio")
    
    if pedido.cantidad <= 0: 
        raise HTTPException(status_code=400,detail='Debe indicar una cantidad')

    db.pedidos.insert_one({
        "producto": pedido.producto,
        "cantidad": pedido.cantidad
    })
    
    return {"msg": "pedido creado"}

@app.get("/pedidos")
def listar_pedidos():

    pedidos = list(
        db.pedidos.find({}, {"_id": 0})
    )
    
    if not pedidos:
        raise HTTPException(status_code=404,detail="No existen pedidos")
    
    return pedidos

@app.get("/articulos")
def art_search(q: str="", page: int = 1, size: int = 10):
    q = quote_plus(q)
    
    return requests.get("http://elasticsearch:9200/articulos/_search",
                        params={"q": q, "from": (page-1) * size, "size": size}).json()

