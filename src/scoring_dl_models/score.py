from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, classification_report, precision_score, accuracy_score, recall_score, f1_score

class_names = ["real", "fake"]
model = AutoModelForSequenceClassification.from_pretrained("ghanashyamvtatti/roberta-fake-news")
tokenizer = AutoTokenizer.from_pretrained("ghanashyamvtatti/roberta-fake-news")

state_dict = torch.load("src/model_api/models/pytorch_model.bin", map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

def predictor(texts):
    outputs = model(**tokenizer(texts, return_tensors="pt", padding=True))
    tensor_logits = outputs[0]
    probas = F.softmax(tensor_logits, -1).detach().numpy()
    return probas

df = pd.read_csv('resources/articles-labeled.csv')
articles = list(df.articles)
labels = list(df.label)

predicted = []
for index, text in tqdm(enumerate(list(df.articles))):
    prob = np.argmax(predictor(text[:1000]))
    predicted.append(prob)

#predicted = (~np.array(predicted).astype(bool)).astype(int)

print(confusion_matrix(labels, predicted))
print(classification_report(labels, predicted))
print()
print(f"Accuracy: {accuracy_score(labels, predicted)}")
print(f"Precision: {precision_score(labels, predicted)}")
print(f"Recall: {recall_score(labels, predicted)}")
print(f"F1-score: {f1_score(labels, predicted)}")

acc_dict = {
    "Accuracy": accuracy_score(labels, predicted),
    "Precision": precision_score(labels, predicted),
    "Recall": recall_score(labels, predicted),
    "F1-score": f1_score(labels, predicted)
}

with open("dashboard/results/confusion_matrix.npy", "wb") as f:
    np.save(f, confusion_matrix(labels, predicted))

with open("dashboard/results/metrics.json", "w") as f:
    json.dump(acc_dict, f)

