import re
from functools import lru_cache

import spacy
import pandas as pd
from typing import List

from nltk import download
from nltk.corpus import stopwords


download('stopwords')


@lru_cache(maxsize=2)
def load_language_model(language: str):
    language_model_map = {
        "english": "en_core_web_trf",
        "portuguese": "pt_core_news_lg"
    }

    model = spacy.load(language_model_map[language])
    return model


def extract_ner_from_sentences(sentences: List[str], language: str) -> pd.DataFrame:
    model = load_language_model(language)
    ner_resume = pd.DataFrame(columns=["entity", "content", "count"])
    for sentence in sentences:
        doc = model(sentence)
        for ent in doc.ents:
            ner_resume = ner_resume.append({
                    "entity": ent.label_,
                    "content": re.sub("\W", " ", ent.text),
                    "count": 1
                },
                ignore_index=True
            )
        yield ner_resume



