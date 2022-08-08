from fastapi import FastAPI
import sqlite3
from typing import List 
from pydantic import BaseModel
import hashlib 
import os
import requests

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pyrebase

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

class User(BaseModel):
    username: str
    password: str



DATABASE_URL = os.path.join("sql/usuarios.sqlite")

app=FastAPI()
security = HTTPBasic()
securityBearer = HTTPBearer()

origins = {
    "https://8000-agustin841155-apirest-kf9c01zz3oe.ws-us53.gitpod.io/",
    "https://8080-agustin841155-apirest-kf9c01zz3oe.ws-us53.gitpod.io/"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
  "apiKey": "AIzaSyDoldPPRHNv-gYWANp06zBix384iGQbQL8",
  "authDomain": "apirest-38082.firebaseapp.com",
  "databaseURL": "https://apirest-38082-default-rtdb.firebaseio.com",
  "projectId": "apirest-38082",
  "storageBucket": "apirest-38082.appspot.com",
  "messagingSenderId": "771162199618",
  "appId": "1:771162199618:web:f82ac63cc50541bd0c7fdb"
}

firebase = pyrebase.initialize_app(firebaseConfig)


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
async def clientes(offset:int=0, limit:int=10, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    user_data = int(db.child("users").child(uid).child("Nivel").get().val())
    if user_data==1:
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
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa a un cliente especifico determinado por el ID",
    description="Regresa un cliente con el ID indicado", 
)
async def clientes_id(id: int, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    user_data = int(db.child("users").child(uid).child("Nivel").get().val())
    if user_data==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
            response = cursor.fetchone()
            return response
    else:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )


#Parte 2

@app.post("/clientes/",response_model=Respuesta, status_code=status.HTTP_202_ACCEPTED,
    summary="A traves del metodo POST se insertan nuevos registos en la base de datos",
    description="Permite añadir un nuevo registro",
) 
async def post_cliente(cliente:ClienteIN, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    user_data = int(db.child("users").child(uid).child("Nivel").get().val())
    if user_data==1: 
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(cliente.nombre,cliente.email))
            response = cursor.fetchone()
            mensaje = {"message" : "Cliente agregado"}
            return mensaje
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.put("/clientes/{id_cliente}",response_model=Respuesta, 
    summary="Permite actualizar un registro a traves del ID indicado en la base de datos",
    description="Permite actualizar un registro a traves del ID ",
)
async def put_cliente(cliente : Cliente, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    user_data = int(db.child("users").child(uid).child("Nivel").get().val())
    if user_data==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(cliente.nombre,cliente.email,cliente.id_cliente))
            response = cursor.fetchone()
            mensaje = {"message" : "Cliente actualizado"}
            return mensaje
    else:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.delete("/clientes/{id_cliente}",response_model=Respuesta, 
    summary="Permite eliminar un registro indicando el ID en la base de datos",
    description="Elimina un registro indicando el ID",
)
async def delete_cliente(id_cliente:int, credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user['users'][0]['localId']
    user_data = int(db.child("users").child(uid).child("Nivel").get().val())
    if user_data==1:
        with sqlite3.connect("sql/clientes.sqlite") as connection:
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
            headers={"WWW-Authenticate": "Bearer"},
        )


#Autenticacion con firebase

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a token for a user",
    description="Get a token for a user",
    tags=["auth"]
)
def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email,password)
        response = {
            "token" : user['idToken']
        }
        return response

    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




@app.get(
    "/user/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get a user",
    description="Get a user",
    tags=["auth"]
)
async def get_user(credentials:HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            "user_data" : user_data
        }
        return response
    
    except Exception as error:
        print(f"ERROR: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


"""agregar usuarios"""

@app.post(
    "/user/insert/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Insertar un nuevo usuario a firebase",
    description="Insertar un nuevo usuario a firebase",
    tags=["Insert"]
)
def insert_user(usuario:User):
    auth = firebase.auth()
    correo = usuario.username
    contrasena = usuario.password

    try:
        user = auth.create_user_with_email_and_password(correo, contrasena)
        Token = user["idToken"]
        userInfo = auth.get_account_info(Token)
        uid = userInfo["users"][0]["localId"]
        email = userInfo["users"][0]["email"]
        data = {"email" : email, "Nivel" : 1}
        db = firebase.database()
        user_data = db.child("users").child(uid).set(data)
        response = {"user": user}
        return response

    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



@app.post(
    "/user/login/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inicio de sesion usando firebase",
    description="Inicio de sesion usando firebase",
    tags=["logIn"],
)
async def login(usuario:User):
    auth = firebase.auth()
    correo = usuario.username
    contrasena = usuario.password
    
    try:
        userData = auth.sign_in_with_email_and_password(correo, contrasena)
        Token = userData["idToken"]
        response = {f"userData": Token}
        return response

    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
