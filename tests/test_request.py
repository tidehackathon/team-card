import json
import requests

text_dict = {"article_text": "To install PyTorch via Anaconda, use the following conda command"}
response = requests.post('http://127.0.0.1/check_fake/', json=text_dict)
