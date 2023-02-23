from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch
from lime.lime_text import LimeTextExplainer

class_names = ["fake", "real"]
model = AutoModelForSequenceClassification.from_pretrained("ghanashyamvtatti/roberta-fake-news")
tokenizer = AutoTokenizer.from_pretrained("ghanashyamvtatti/roberta-fake-news")
state_dict = torch.load("models/pytorch_model.bin", map_location=torch.device('cpu'))
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


def get_explanation(text):
    """Returns an explanation of the model results for the given text.

    Args:
        text (str): Article text in string format.

    Returns:
        explanation (list): a list of important words and their impact scores.
    """
    explainer = LimeTextExplainer(class_names=class_names)
    exp = explainer.explain_instance(text, predictor, num_features=10, num_samples=20)
    return exp.as_list()

