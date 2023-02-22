import requests

dl_test_dict = {"article_text": "To install PyTorch via Anaconda, use the following conda command"}
matching_test_dict = {"message_text": "i think some are actual russian bots to antagonize other nations citizens against ukraine to support russia"}

def test_dl_info():
    response = requests.get("http://127.0.0.1:11111/")
    assert response.status_code == 200
    assert response.json() == {"info": "This is a disinformation detection deep learning model API"}

def test_matching_info():
    response = requests.get("http://127.0.0.1:22222/")
    assert response.status_code == 200
    assert response.json() == {"info": "This is a disinformation detection text matching model API"}

def test_dl_model():
    response = requests.post('http://127.0.0.1:11111/check_fake/', json=dl_test_dict)
    assert response.status_code == 200
    assert response.json().get('result') == False

def test_matching_model():
    response = requests.post('http://127.0.0.1:22222/match_fake/', json=matching_test_dict)
    assert response.status_code == 200
    print(response.json()[0].get('score'))
    assert response.json()[0].get('score') == 0.9054368138313293

