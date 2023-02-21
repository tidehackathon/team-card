import numpy as np
import heapq
import json
from operator import itemgetter
from sentence_transformers import SentenceTransformer

with open('embeddings/cases_embeddings.npy', 'rb') as f:
    cases_embeddings = np.load(f)
    
with open('embeddings/cases_content.json', "r") as f:
    cases_content = json.load(f)

query = "Hugging Face makes it easy to collaboratively build and showcase your Sentence Transformers models! You can collaborate with your organization, upload and showcase your own models in your profile"
model = SentenceTransformer('bert-base-nli-mean-tokens')
cases_text = [item['content'] for item in cases_content]
    

def cosined(a,b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_top_n(diction, n):
    topitems = heapq.nlargest(n, diction.items(), key=itemgetter(1))
    return dict(topitems)

def get_top_similar(query, n=5):
    query_encoded = model.encode(query)

    cases_dictionary = dict(zip(cases_text, cases_embeddings))
    distances = [cosined(query_encoded, cases_dictionary[key]) for key in cases_dictionary.keys()]
    distance_dictionary = dict(zip(cases_text, distances))
    
    if query in distance_dictionary.keys():
        _ = distance_dictionary.pop(query)
    
    top_cases = get_top_n(distance_dictionary, n)
    results = []
    for key in top_cases.keys():
        results.append({
            "score": top_cases.get(key),
            "title": [item.get("title") for item in cases_content if item.get("content") == key][0],
            "content": key
        })
    return results



