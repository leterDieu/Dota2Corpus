import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


tokenizer = AutoTokenizer.from_pretrained('textdetox/bert-multilingual-toxicity-classifier')
model = AutoModelForSequenceClassification.from_pretrained('textdetox/bert-multilingual-toxicity-classifier')


def count_toxicity(chat_refactored):
    toxicity_dict = {}
    for i in chat_refactored:
        batch = tokenizer.encode(i['key'], return_tensors="pt")
        output = model(batch)
        probs = torch.softmax(output.logits, dim=-1)
        if i['slot'] not in toxicity_dict:
            toxicity_dict[str(i['slot'])] = [probs.tolist()[0][1], 1]
        else:
            toxicity_dict[str(i['slot'])][0] += probs.tolist()[0][1]
            toxicity_dict[str(i['slot'])][1] += 1
    for i in toxicity_dict:
        toxicity_dict[i] = toxicity_dict[i][0] / toxicity_dict[i][1]
    return toxicity_dict
