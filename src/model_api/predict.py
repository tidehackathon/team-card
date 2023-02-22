from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from lime.lime_text import LimeTextExplainer
import numpy as np

class_names = ["real", "fake"]
model = AutoModelForSequenceClassification.from_pretrained("ghanashyamvtatti/roberta-fake-news")
tokenizer = AutoTokenizer.from_pretrained("ghanashyamvtatti/roberta-fake-news")

#tokenizer = AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")
#model = AutoModelForSequenceClassification.from_pretrained("mrm8488/bert-tiny-finetuned-fake-news-detection")

#tokenizer = AutoTokenizer.from_pretrained("jy46604790/Fake-News-Bert-Detect")
#model = AutoModelForSequenceClassification.from_pretrained("jy46604790/Fake-News-Bert-Detect")


def predictor(texts):
    outputs = model(**tokenizer(texts, return_tensors="pt", padding=True))
    tensor_logits = outputs[0]
    probas = F.softmax(tensor_logits, -1).detach().numpy()
    return probas


def get_explanation(text):
    explainer = LimeTextExplainer(class_names=class_names)
    exp = explainer.explain_instance(text, predictor, num_features=10, num_samples=20)
    return exp.as_list()

