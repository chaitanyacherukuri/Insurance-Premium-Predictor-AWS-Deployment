import pytest
from fastapi.testclient import TestClient
from app import app

# Create TestClient fixture
@pytest.fixture
def client():
    return TestClient(app)

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Insurance Premium Predictor API'}

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
    assert response.json()['version'] == '1.0.0'
    assert isinstance(response.json()['model_loaded'], bool)

def test_predict(client):
    data = {
        "age": 31,
        "weight": 81,
        "height": 1.75,
        "income_lpa": 21,
        "smoker": True,
        "city": "Mumbai",
        "occupation": "private_job"
    }
    response = client.post('/predict', json=data)
    assert response.status_code == 200
    assert response.json() == {"response": 
                               {"predicted_category": "Low", "confidence": 0.75, 
                                "class_probabilities": {"High": 0,
                                                        "Low": 0.75,
                                                        "Medium": 0.25
                                                        }
                                                    }
                                                }
