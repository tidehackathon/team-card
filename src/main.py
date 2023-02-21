from predict import predictor, get_explanation
from langdetect import detect
import pandas as pd
import numpy as np


df = pd.read_csv("resources/articles.csv", encoding="utf8")
data = list(df.articles)

class_dict = {0: "fake", 1: "neutral"}

sums = 0
alltexts = 0
for text in data:
    if detect(text) != 'en':
        continue
    try:
        prob = predictor(text)
        print(class_dict.get(np.argmax(prob)))
        print(prob)
        print()
        alltexts += 1
        sums += np.argmax(prob)
    except:
        print("error")
        continue

print(f"{sums}/{alltexts} were real: {(sums/alltexts)*100}%")

