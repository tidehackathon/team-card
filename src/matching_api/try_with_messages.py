import pandas as pd
from tqdm import tqdm
from model import get_top_similar

df = pd.read_csv("~/Desktop/TIDE2023/data/messages-preprocessed.csv")

scores = []
for message in tqdm(list(df.content)[:10000]):
    res = get_top_similar(message)
    best_score = res[0].get('score')
    if best_score < 0.9:
        continue
    print(f"MESSAGE: {message}")
    print(f"SCORE: {best_score}")
    print(f"CASE: {res[0].get('title')}")
    scores.append(best_score)
    print()

