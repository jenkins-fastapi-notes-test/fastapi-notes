from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_note():
    response = client.post("/notes", json={"title": "Test", "content": "Hello"})
    assert response.status_code == 200

def test_get_notes():
    response = client.get("/notes")
    assert response.status_code == 200
    

def test_get_note_by_id():
    response = client.post("/notes", json={"title": "Some Note", "content": "ABCDEF"})
    data = response.json()
    response = client.get(f"/notes/{data["id"]}")
    assert response.status_code == 200

def test_delete_note():
    response = client.post("/notes", json={"title": "Some Note", "content": "ABCDEF"})
    data = response.json()
    response = client.delete(f"/notes/{data["id"]}")
    assert response.status_code == 200
    assert response.json()["deleted"] == True