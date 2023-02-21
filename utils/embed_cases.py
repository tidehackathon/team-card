import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import warnings
import json

df = pd.read_csv("resources/disinfo_cases.csv")
unique_cases_upper = np.array(df.case)
cases_titles = np.array(df.title)

cases_diction = []
for index, title in enumerate(cases_titles):
    cases_diction.append({"title": title,
                          "content": unique_cases_upper[index]})

df = df.replace(to_replace=r'\n', value='', regex=True)
df = df.replace(to_replace=r'\r', value='', regex=True)
df['case'] = df.case.str.lower()
unique_cases = list(df.case)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = model.encode(unique_cases)

with open('src/matching_api/embeddings/cases_embeddings.npy', 'wb') as f:
    np.save(f, sentence_embeddings)

with open('src/matching_api/embeddings/cases_content.json', 'w') as f:
    json.dump(cases_diction, f)
