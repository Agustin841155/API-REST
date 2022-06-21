from fastapi.testclient import TestClient
import json

from code.main import app

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API REST"}

def test_clientes():
    response = clientes.get("/clientes/")
    assert response.status_code == 200
    assert response.json() == [{"id_cliente":1,"nombre":"Dejah","email":"dejah@gmail.com"},
    {"id_cliente":2,"nombre":"John","email":"john@gmail.com"}, {"id_cliente":3,"nombre":"Carthoris","email":"carthoris@gmail.com"}]
    
def test_clientes_id():
    response = clientes.get('/clientes/1')
    data = [{"id_cliente":1,"nombre":"Dejah","email":"dejah@gmail.com"}]
    assert response.status_code == 200
    assert response.json() == data

def test_post_cliente():
    payload = {"id_cliente":4,"nombre":"agus", "email": "agus@gmail.com"}
    response = clientes.post("/clientes/", json=payload) 
    Response = {"message" : "Cliente agregado"}
    assert response.status_code == 200
    assert response.json() == Response

def test_put_cliente():
    payload = {"id_cliente":4,"nombre" : "Agustin", "email" : "agustin@gmail.com"}
    response = clientes.put("/clientes/",json=payload)
    Response = {"message" : "Cliente actualizado"}
    assert response.status_code == 200
    assert response.json() == Response

def test_delete_cliente():
    response = clientes.delete("/clientes/4")
    Response = {"message" : "Cliente borrado"}
    assert response.status_code == 200
    assert response.json() == Response