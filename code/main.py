from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel
import hashlib 
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre:str
    email:str

class Usuarios(BaseModel):
    username: str
    level: int

DATABASE_URL = os.path.join("sql/usuarios.sqlite")

app=FastAPI()
security = HTTPBasic()

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API REST"}

@app.get("/clientes/",
    response_model=List[Cliente],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de todos los clientes en la base de datos",
    description="Regresa una lista de todos los clientes clientes",
)
async def clientes(offset:int=0, limit:int=10, level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?", (limit,offset)) 
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id}", response_model=List[Cliente], status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa a un cliente especifico determinado por el ID",
    description="Regresa un cliente con el ID indicado", 
)
async def clientes_id(id: int, level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
            response = cursor.fetchall()
            return response
    else:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

#Parte 2

@app.post("/clientes/",response_model=Respuesta, status_code=status.HTTP_202_ACCEPTED,
    summary="A traves del metodo POST se insertan nuevos registos en la base de datos",
    description="Permite añadir un nuevo registro",
) 
async def post_cliente(nombre:str,email:str, level: int = Depends(get_current_level)):
    if level==0: 
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(nombre,email))
            response = cursor.fetchone()
            mensaje = {"message" : "Cliente agregado"}
            return mensaje
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/{id_cliente}",response_model=Respuesta, 
    summary="Permite actualizar un registro a traves del ID indicado en la base de datos",
    description="Permite actualizar un registro a traves del ID ",
)
async def put_cliente(id_cliente:int,nombre:str,email:str, level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(nombre,email,id_cliente))
            response = cursor.fetchone()
            mensaje = {"message" : "Cliente actualizado"}
            return mensaje
    else:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id_cliente}",response_model=Respuesta, 
    summary="Permite eliminar un registro indicando el ID en la base de datos",
    description="Elimina un registro indicando el ID",
)
async def delete_cliente(id_cliente:int, level: int = Depends(get_current_level)):
    if level==0:
        with sqlite3.connect("code/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(id_cliente))
            response = cursor.fetchone()
            mensaje = {"message" : "Cliente borrado"}
            return mensaje
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )