import numpy as np
import heapq
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter
from sentence_transformers import SentenceTransformer

# Reading precomputed embeddings for all disinformation cases
with open('embeddings/cases_embeddings.npy', 'rb') as f:
    cases_embeddings = np.load(f)

# Reading the disinformation cases contents 
with open('embeddings/cases_content.json', "r") as f:
    cases_content = json.load(f)

# Loading BERT sentence embeddings model from: https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens
model = SentenceTransformer('bert-base-nli-mean-tokens')
cases_text = [item['content'] for item in cases_content]

# Query used only for testing
query = "i think some are actual russian bots to antagonize other nations citizens against ukraine to support russia"


def remove_stopwords(sentence):
    """Removes stop words from the given sentence.

    Args:
        sentence (str): a sentences from which the stop words are going to be removed.

    Returns:
        sentence (str): the same sentence without stop words.
    """
    return " ".join([word for word in sentence if word not in set(stopwords.words('english'))])


def cosined(a, b):
    """Computes cosine distance between the given vectors a and b.

    Args:
        a, b (ndarray): numpy arrays of floats.

    Returns:
        distance (float): the cosine distance between a and b.
    """
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))


def get_top_n(diction, n=10):
    """Returns top n items from the dictionary.

    Args:
        diction (dict): a dictionary of case embeddings and its distance from the query.
        n (int): a number of top items to select.

    Returns:
        topitems (dict): a dictionary with selected top n items.
    """
    topitems = heapq.nlargest(n, diction.items(), key=itemgetter(1))
    return dict(topitems)

def get_top_similar(query, thresh=0.88):
    """Returns a list of dictionaries with matched closes disinformation cases.

    Args:
        query (str): a message in a string format.
        thresh (float): a threshold by which the selected cases are filtered.

    Returns:
        results (list): a list of dictionaries of selected disinformation cases.
                        Score shows the matching score [0, 1], where 1 is the most similar.
                        Title shows the title of the matched disinformation case.
                        Content shows the disinformation case text.

    """
    query = remove_stopwords(word_tokenize(query)).lower()
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
            "score": round(float(top_cases.get(key)),3),
            "title": [item.get("title") for item in cases_content if item.get("content") == key][0],
            "content": key
        })
    return results



