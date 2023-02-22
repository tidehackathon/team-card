import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, classification_report, precision_score, accuracy_score, recall_score, f1_score
from ..model_api.predict import predictor

df = pd.read_csv('resources/articles-labeled.csv')
class_dict = {0: "neutral", 1: "fake"}
articles = list(df.articles)
labels = list(df.label)

predicted = []
for index, text in tqdm(enumerate(list(df.articles))):
    prob = np.argmax(predictor(text[:1000]))
    predicted.append(prob)

predicted = (~np.array(predicted).astype(bool)).astype(int)

print(confusion_matrix(labels, predicted))
print(classification_report(labels, predicted))
print()
print(f"Accuracy: {accuracy_score(labels, predicted)}")
print(f"Precision: {precision_score(labels, predicted)}")
print(f"Recall: {recall_score(labels, predicted)}")
print(f"F1-score: {f1_score(labels, predicted)}")

