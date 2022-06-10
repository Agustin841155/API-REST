from fastapi.testclient import testclient

from main import app

clientes = TestClient(app)

def test_index():
    response = clientes("/")
    assert response.status_code == 200
    assert response.json() == {"mesagge": "Hello world"}