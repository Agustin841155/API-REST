from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre:str
    email:str

app=FastAPI()

@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API REST"}

@app.get("/clientes/",response_model=List[Cliente])
async def clientes(offset:int=0, limit:int=10):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?", (limit,offset)) 
        response = cursor.fetchall()
        return response 

@app.get("/clientes/{id}")
async def clientes_id(id):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
        response = cursor.fetchall()
        return response 

#Parte 2

@app.post("/clientes/",response_model=Respuesta) 
async def post_cliente(nombre:str,email:str): 
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(nombre,email))
        response = cursor.fetchone()
        mensaje = {"message" : "Cliente agregado"}
        return mensaje

@app.put("/clientes/{id_cliente}",response_model=Respuesta)
async def put_cliente(id_cliente:int,nombre:str,email:str):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(nombre,email,id_cliente))
        response = cursor.fetchone()
        mensaje = {"message" : "Cliente actualizado"}
        return mensaje       

@app.delete("/clientes/{id_cliente}",response_model=Respuesta)
async def delete_cliente(id_cliente:int):
   with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(id_cliente))
        response = cursor.fetchone()
        mensaje = {"message" : "Cliente borrado"}
        return mensaje