_sentence_import = {
    "exchange": "NLEaser",
    "queue": "nleaser_worker_sentence_import",
    "routing_key": "NLEaser.nleaser_worker_sentence_import",
}

_wordcloud_create = {
    "exchange": "NLEaser",
    "queue": "nleaser_worker_wordcloud_create",
    "routing_key": "NLEaser.nleaser_worker_wordcloud_create",
}

_ngrams_create = {
    "exchange": "NLEaser",
    "queue": "nleaser_worker_ngrams_create",
    "routing_key": "NLEaser.nleaser_worker_ngrams_create",
}
_ner_resume_create = {
    "exchange": "NLEaser",
    "queue": "ner_resume_create",
    "routing_key": "NLEaser.ner_resume_create"
}


QUEUES = {
    "NLEaser.nleaser_worker_sentence_import": _sentence_import,
    "NLEaser.nleaser_worker_wordcloud_create": _wordcloud_create,
    "NLEaser.nleaser_worker_ngrams_create": _ngrams_create,
    "NLEaser.ner_resume_create": _ner_resume_create
}


def get_queue_config(queue_name):
    return QUEUES[queue_name]