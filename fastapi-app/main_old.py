from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os, requests

app = FastAPI(title="API NoSQL (vulnerable)")
mongo = MongoClient(os.getenv("MONGO_HOST","mongo"), 27017)
db = mongo[os.getenv("MONGO_DATABASE","tienda")]

class Login(BaseModel): username: str; password: str
class Pedido(BaseModel): producto: str; cantidad: int

@app.post("/login_mongo")
async def login(req: Request):
    data = await req.json()
    # ❌ NoSQLi: acepta operadores $ en credenciales
    user = db.usuarios.find_one({"username": data.get("username"),
                                 "password": data.get("password")}, {"_id":0})
    if user: return {"msg":"ok"}
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
def art_search(q: str="*"):
    return requests.get("http://elasticsearch:9200/articulos/_search",
                        params={"q": q}).json()

