import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from langdetect import detect
tokenizer = AutoTokenizer.from_pretrained('textdetox/bert-multilingual-toxicity-classifier')
model = AutoModelForSequenceClassification.from_pretrained('textdetox/bert-multilingual-toxicity-classifier')

def detect_lang(word):
    b = detect(word)
    return b

def split_sentence(sentence):
    words = sentence.split()
    groups = []
    current_group = []
    current_lang = None
    langs = []

    for word in words:
        if word:
            lang = detect_lang(word)
        else:
            lang = 'unknown'
        if lang not in langs:
            langs.append(lang)
        if lang != current_lang:
            if current_group:
                groups.append((' '.join(current_group), current_lang))
            current_group = [word]
            current_lang = lang
        else:
            current_group.append(word)

    if current_group:
        groups.append((' '.join(current_group), current_lang))

    return groups, len(langs)

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
print(split_sentence('go сын бляди for your mother'))