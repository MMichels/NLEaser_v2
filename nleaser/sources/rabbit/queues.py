_sentence_import = {
    "exchange": "NLEaser",
    "queue": "sentence_import",
    "routing_key": "NLEaser.sentence_import",
}

_wordcloud_create = {
    "exchange": "NLEaser",
    "queue": "_wordcloud_create",
    "routing_key": "NLEaser._wordcloud_create",
}

_ngrams_create = {
    "exchange": "NLEaser",
    "queue": "ngrams_create",
    "routing_key": "NLEaser.ngrams_create",
}
_ner_resume_create = {
    "exchange": "NLEaser",
    "queue": "ner_resume_create",
    "routing_key": "NLEaser.ner_resume_create"
}


QUEUES = {
    "NLEaser.sentence_import": _sentence_import,
    "NLEaser.wordcloud_create": _wordcloud_create,
    "NLEaser.ngrams_create": _ngrams_create,
    "NLEaser.ner_resume_create": _ner_resume_create
}

def get_queue_config(queue_name):
    return QUEUES[queue_name]