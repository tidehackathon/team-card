import numpy as np
import heapq
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter
from sentence_transformers import SentenceTransformer

with open('embeddings/cases_embeddings.npy', 'rb') as f:
    cases_embeddings = np.load(f)
    
with open('embeddings/cases_content.json', "r") as f:
    cases_content = json.load(f)

model = SentenceTransformer('bert-base-nli-mean-tokens')
cases_text = [item['content'] for item in cases_content]

# Query for testing
query = "i think some are actual russian bots to antagonize other nations citizens against ukraine to support russia"


def remove_stopwords(sentence):
    return " ".join([word for word in sentence if word not in set(stopwords.words('english'))])

def cosined(a,b):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_top_n(diction, n=10):
    topitems = heapq.nlargest(n, diction.items(), key=itemgetter(1))
    return dict(topitems)

def get_top_similar(query, thresh=0.88):
    query = remove_stopwords(word_tokenize(query))
    query_encoded = model.encode(query)

    cases_dictionary = dict(zip(cases_text, cases_embeddings))
    distances = [cosined(query_encoded, cases_dictionary[key]) for key in cases_dictionary.keys()]
    distance_dictionary = dict(zip(cases_text, distances))
    
    if query in distance_dictionary.keys():
        _ = distance_dictionary.pop(query)
    
    top_cases = get_top_n(distance_dictionary, 20)
    results = []
    for key in top_cases.keys():
        if top_cases.get(key) < thresh:
            continue
        results.append({
            "score": float(top_cases.get(key)),
            "title": [item.get("title") for item in cases_content if item.get("content") == key][0],
            "content": key
        })
    return results



