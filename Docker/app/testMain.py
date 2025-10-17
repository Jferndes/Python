import pytest
import pandas as pd
import json
import main

@pytest.fixture
def initial_df():
    return pd.DataFrame(
        [
            {"id": 1, "nom": "Alice", "age": 25, "score": 88.0},
            {"id": 2, "nom": "Bob", "age": 30, "score": 75.0},
            {"id": 3, "nom": "Charlie", "age": 22, "score": 95.0},
        ]
    )

@pytest.fixture
def app_mem(initial_df, tmp_path, monkeypatch):
    """App en mémoire (pas d'I/O disque)"""
    # Créer un fichier CSV temporaire
    csv_path = tmp_path / "score.csv"
    initial_df.to_csv(csv_path, index=False)
    
    # Fonction mock pour remplacer load_data
    def mock_load_data():
        return pd.read_csv(csv_path)
    
    # Patcher la fonction load_data dans le module main
    monkeypatch.setattr(main, 'load_data', mock_load_data)
    
    main.app.config.update({"TESTING": True})
    
    # pour garder app on et la nettoyer à la fin des tests
    yield main.app

@pytest.fixture
def client(app_mem):
    """Client de test"""
    with app_mem.test_client() as client:
        yield client

# Tests pour GET /api/v1/scores
def test_get_scores_success(client):
    """Test récupération de tous les scores"""
    response = client.get('/api/v1/scores')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['nom'] == 'Alice'
    assert data[0]['score'] == 88.0
    assert data[1]['nom'] == 'Bob'
    assert data[1]['score'] == 75.0
    assert data[2]['nom'] == 'Charlie'
    assert data[2]['score'] == 95.0

# Tests pour GET /api/v1/scores/stats
def test_get_stats_success(client):
    """Test des statistiques sur les scores"""
    response = client.get('/api/v1/scores/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'mean' in data
    assert 'median' in data
    assert 'std' in data
    assert data['mean'] == pytest.approx(86.0, 0.1)
    assert data['median'] == 88.0
    assert data['std'] > 0

# Tests pour GET /api/v1/scores/<int:score_id>
def test_get_score_superior_success(client):
    """Test récupération des scores supérieurs à un seuil"""
    response = client.get('/api/v1/scores/80')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert all(item['score'] > 80 for item in data)
    assert data[0]['nom'] == 'Alice'
    assert data[1]['nom'] == 'Charlie'

def test_get_score_superior_one_result(client):
    """Test avec un seul résultat"""
    response = client.get('/api/v1/scores/90')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['nom'] == 'Charlie'
    assert data[0]['score'] == 95.0

def test_get_score_superior_no_results(client):
    """Test sans résultat (404)"""
    response = client.get('/api/v1/scores/100')
    assert response.status_code == 404

def test_get_score_superior_all_results(client):
    """Test avec tous les résultats"""
    response = client.get('/api/v1/scores/50')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3

# Tests pour POST /api/v1/scores
def test_add_score_success(client):
    """Test ajout d'un score avec succès"""
    new_score = {
        "nom": "David",
        "age": 28,
        "score": 92.0
    }
    response = client.post('/api/v1/scores', 
                          data=json.dumps(new_score),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['nom'] == 'David'
    assert data['age'] == 28
    assert data['score'] == 92.0
    assert data['id'] == 4

def test_add_score_missing_nom(client):
    """Test sans nom (400)"""
    new_score = {
        "age": 28,
        "score": 92.0
    }
    response = client.post('/api/v1/scores',
                          data=json.dumps(new_score),
                          content_type='application/json')
    assert response.status_code == 400

def test_add_score_missing_age(client):
    """Test sans âge (400)"""
    new_score = {
        "nom": "David",
        "score": 92.0
    }
    response = client.post('/api/v1/scores',
                          data=json.dumps(new_score),
                          content_type='application/json')
    assert response.status_code == 400

def test_add_score_missing_score(client):
    """Test sans score (400)"""
    new_score = {
        "nom": "David",
        "age": 28
    }
    response = client.post('/api/v1/scores',
                          data=json.dumps(new_score),
                          content_type='application/json')
    assert response.status_code == 400

def test_add_score_empty_body(client):
    """Test avec body vide (400)"""
    response = client.post('/api/v1/scores',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400

def test_add_multiple_scores(client):
    """Test ajout de plusieurs scores"""
    scores = [
        {"nom": "David", "age": 28, "score": 92.0},
        {"nom": "Emma", "age": 24, "score": 87.0}
    ]
    
    for score in scores:
        response = client.post('/api/v1/scores',
                              data=json.dumps(score),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)

        assert data['nom'] == score['nom']
        assert data['age'] == score['age']