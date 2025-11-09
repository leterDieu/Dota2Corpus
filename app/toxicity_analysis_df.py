import pandas as pd
import language_tool_python
from langdetect import detect, DetectorFactory

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import time
import string
import re

DetectorFactory.seed = 0

tokenizer = AutoTokenizer.from_pretrained('textdetox/bert-multilingual-toxicity-classifier', n_jobs=-1)
model = AutoModelForSequenceClassification.from_pretrained('textdetox/bert-multilingual-toxicity-classifier')

tool_en = language_tool_python.LanguageTool('en')
tool_ru = language_tool_python.LanguageTool('ru')
tool_es = language_tool_python.LanguageTool('es')

match_codes = {
    'ru': tool_ru,
    'uk': tool_ru,
    'mk': tool_ru,
    'sk': tool_ru,
    'sl': tool_ru,
    'en': tool_en,
}

iter = 0

def match_code_func(code: str | None) -> language_tool_python.server.LanguageTool:
    global iter
    print(iter)
    iter += 1
    if code is None:
        return tool_en
    if code not in match_codes:
        return tool_en
    return match_codes[code]


def chat_to_lang(x: str) -> str | None:
    x_no_numbers = ''.join([i for i in str(x) if not i.isdigit()])
    x_no_puct = re.sub(r'[^\w\s]','',x_no_numbers).replace('?', '').replace(' ', '')
    return detect(x) if (isinstance(x, str) and len(x_no_puct) >= 2) else None
    
def chat_to_correct_chat(x: str) -> str | None:
    lang = chat_to_lang(x)
    return match_code_func(lang).correct(x) if lang is not None else None
    
def get_toxicity(x: str | None) -> float | None:
    if x is None:
        return None
    if len(x) >= 512:
        x = x[:511]
    try:
        batch = tokenizer.encode(x, return_tensors="pt")
        output = model(batch)
        probs = torch.softmax(output.logits, dim=-1)
        return probs.tolist()[0][1]
    except:
        return None


df = pd.read_csv('players_info_all.csv', index_col=0)

df['language'] = df['chat'].apply(lambda x: chat_to_lang(x))

df['correct_chat'] = df['chat'].apply(lambda x: chat_to_correct_chat(x))

df['toxicity_context_2'] = df['correct_chat'].apply(lambda x: get_toxicity(x))

df.to_csv('players_info_all_2.csv')

tool_ru.close()
tool_en.close()
tool_es.close()


