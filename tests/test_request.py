import json
import requests

text_dict = {"article_text": "Donald Trump Sends Out Embarrassing New Years Eve Message; This is Disturbing,Donald Trump just couldn t wish all Americans a Happy New Year and leave it at that"}
#text_dict = {"message_text": "i think some are actual russian bots to antagonize other nations citizens against ukraine to support russia",
#             "threshold": 0.88}
#response = requests.post('http://127.0.0.1:22222/match_fake/', json=text_dict)
response = requests.post('http://127.0.0.1:11111/check_fake/', json=text_dict)
