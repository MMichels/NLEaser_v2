from typing import List

import pandas as pd
import numpy as np

from nltk import download
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


download('stopwords')


def generate_ngrams(sentences: List[str], size: int, language: str) -> pd.DataFrame:
    sw = stopwords.words(language)
    vec = CountVectorizer(min_df=5, max_df=0.8, max_features=10000, stop_words=sw, ngram_range=(size, size))
    tfidf = TfidfTransformer(norm='l1')

    bag_of_words = vec.fit_transform(sentences)
    words_relevance_by_sentences: np.ndarray = tfidf.fit_transform(bag_of_words)

    sum_words_ocurrences = bag_of_words.sum(axis=0)
    sum_words_relevances = words_relevance_by_sentences.sum(axis=0)
    max_relevance = sum_words_relevances[0].max()

    words_freq_relevance = [
        (word, sum_words_ocurrences[0, idx], ((sum_words_relevances[0, idx]) / max_relevance))
        for word, idx in vec.vocabulary_.items()
    ]

    words_freq_relevance = pd.DataFrame(
        words_freq_relevance,
        columns=["content", "count", "relevance"]
    )

    return words_freq_relevance
