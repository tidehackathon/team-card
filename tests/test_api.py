from fastapi.testclient import TestClient
import requests
from src.api import app

client = TestClient(app)

text_dict = {"article_text": "To install PyTorch via Anaconda, use the following conda command"}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"info": "This is a disinformation detection model API"}


def test_r_model():
    response = requests.post('http://127.0.0.1:8000/check_fake/', json=text_dict)
    assert response.status_code == 200
    assert response.json() == {"result": False}

