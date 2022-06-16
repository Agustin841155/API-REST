from fastapi.testclient import TestClient


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
