from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, classification_report, precision_score, accuracy_score, recall_score, f1_score
from ..data_preprocessing.articles_prep import preprocess_article

# Load finetuned fake news model
model = AutoModelForSequenceClassification.from_pretrained("ghanashyamvtatti/roberta-fake-news")
tokenizer = AutoTokenizer.from_pretrained("ghanashyamvtatti/roberta-fake-news")
state_dict = torch.load("src/model_api/models/pytorch_model.bin", map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

def predictor(texts):
    """Returns an array of probabilities that the given text belongs to each of the class.

    Args:
        texts (str): Article text in string format.

    Returns:
        probas (ndarray): and array of probabilities for each class: fake (at index 0), real (at index 1)
    """
    outputs = model(**tokenizer(texts, return_tensors="pt", padding=True))
    tensor_logits = outputs[0]
    probas = F.softmax(tensor_logits, -1).detach().numpy()
    return probas

# Read and preprocess the articles used for testing. The location of the test file must always be: 
# resources/articles-test.csv
df = pd.read_csv('resources/articles-test.csv')
df['article'] = df["article"].apply(preprocess_article)
articles = list(df.article)
labels = list(df.label)

# Get the predictions for each line in csv
predicted = []
for index, text in tqdm(enumerate(list(df.article))):
    prob = np.argmax(predictor(text[:1000]))
    predicted.append(prob)

confusionmat = confusion_matrix(labels, predicted)
acc = accuracy_score(labels, predicted)
prec = precision_score(labels, predicted)
recall = recall_score(labels, predicted)
f1score = f1_score(labels, predicted)

# Print the results
print(confusionmat)
print(classification_report(labels, predicted))
print()
print(f"Accuracy: {acc}")
print(f"Precision: {prec}")
print(f"Recall: {recall}")
print(f"F1-score: {f1score}")

# Save the results for visualizations
acc_dict = {
    "Accuracy": acc,
    "Precision": prec,
    "Recall": recall,
    "F1-score": f1score
}

with open("dashboard/results/confusion_matrix.npy", "wb") as f:
    np.save(f, confusion_matrix(labels, predicted))

with open("dashboard/results/metrics.json", "w") as f:
    json.dump(acc_dict, f)
