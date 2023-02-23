# A file to manually test the APIs requests
import requests

article_request_dict = {"article_text": "The apple is"}
message_request_dict = {"message_text": "i think some are actual russian bots to antagonize other nations citizens against ukraine to support russia",
             "threshold": 0.88}

# Deep learning disinformation model API test request
disinfo_response = requests.post('http://127.0.0.1:11111/check_fake/', json=article_request_dict)

# Cases matching model API test request
match_response = requests.post('http://127.0.0.1:22222/match_fake/', json=message_request_dict)

# Printing results
print(disinfo_response.text)
print(match_response.text)
