import requests


def api_request_info():
    response = requests.get('http://disinfo_api:80/')
    return response.text


def model_request(article_text):
    text_dict = {"article_text": article_text}
    response = requests.post('http://disinfo_api:80/check_fake/', json=text_dict)
    return response


def case_matching(message_text):
    text_dict = {"message_text": message_text}
    response = requests.post('http://match_api:80/match_fake/', json=text_dict)
    return response
