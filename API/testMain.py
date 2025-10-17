import pytest
from main import app, TODOS


@pytest.fixture
def client():
    """Crée un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_todos():
    """Réinitialise les données avant chaque test"""
    TODOS.clear()
    TODOS.extend([
        {"id": 1, "title": "Acheter du pain", "done": False},
        {"id": 2, "title": "Lire Flask docs", "done": True},
    ])


def test_list_todos(client):
    """Test GET /todos - Liste tous les todos"""
    response = client.get('/todos')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Acheter du pain"


def test_get_todo_success(client):
    """Test GET /todos/<id> - Récupère un todo existant"""
    response = client.get('/todos/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["title"] == "Acheter du pain"
    assert data["done"] is False


def test_get_todo_not_found(client):
    """Test GET /todos/<id> - Todo inexistant"""
    response = client.get('/todos/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_todo_success(client):
    """Test POST /todos - Crée un nouveau todo"""
    response = client.post('/todos', json={"title": "Nouveau todo"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 3
    assert data["title"] == "Nouveau todo"
    assert data["done"] is False


def test_create_todo_missing_title(client):
    """Test POST /todos - Sans titre"""
    response = client.post('/todos', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_update_todo_title(client):
    """Test PATCH /todos/<id> - Modifie le titre"""
    response = client.patch('/todos/1', json={"title": "Titre modifié"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Titre modifié"
    assert data["done"] is False


def test_update_todo_done(client):
    """Test PATCH /todos/<id> - Marque comme fait"""
    response = client.patch('/todos/1', json={"done": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["done"] is True


def test_update_todo_not_found(client):
    """Test PATCH /todos/<id> - Todo inexistant"""
    response = client.patch('/todos/999', json={"title": "Test"})
    assert response.status_code == 404


def test_delete_todo_success(client):
    """Test DELETE /todos/<id> - Supprime un todo"""
    response = client.delete('/todos/1')
    assert response.status_code == 204
    
    # Vérifie que le todo a été supprimé
    response = client.get('/todos')
    data = response.get_json()
    assert len(data) == 1


def test_delete_todo_not_found(client):
    """Test DELETE /todos/<id> - Todo inexistant"""
    response = client.delete('/todos/999')
    assert response.status_code == 404