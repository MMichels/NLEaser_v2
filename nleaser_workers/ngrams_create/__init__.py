import json
import logging
from typing import List

from pandas import DataFrame
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from nleaser_models.nlp.ngrams import ExtractedNGramsModel, ExtractedNGramsSchema
from nleaser_models.sentence import SentenceModel
from nleaser_models.tasks.ngrams import NGramsCreateTaskModel
from nleaser_models.user import UserModel
from nleaser_sources.services.nlp.tfidf.ngrams import generate_ngrams
from nleaser_sources.services.cipher import load_cipher

logger = logging.getLogger('nleaser_worker_ngrams_create')


def extract_ngrams(user: UserModel, sentences: List[SentenceModel], size: int, language: str) -> DataFrame:
    cipher = load_cipher(user)
    pre_processed_sentences = [
        cipher.decrypt(sentence.pre_processed_content.encode()).decode()
        for sentence in sentences
    ]
    ngrams = generate_ngrams(pre_processed_sentences, size, language)
    return ngrams


def process_task(ngram_create_task: NGramsCreateTaskModel) -> bool:
    ngram_create_task.status = "in_progress"
    ngram_create_task.total = 3
    ngram_create_task.save()

    # Recupera as sentenças

    try:
        sentences: List[SentenceModel] = SentenceModel.objects(
            datafile=ngram_create_task.datafile
        ).all()
        ngram_create_task.progress = 1
        ngram_create_task.save()
    except Exception as e:
        ngram_create_task.status = "error"
        ngram_create_task.error = "Erro ao importar as sentenças desse arquivo"
        ngram_create_task.save()
        logger.error(
            ngram_create_task.error,
            exc_info=True,
            extra={"received_args": ngram_create_task.to_mongo()}
        )
        return False

    # Extrai os ngrams
    try:
        ngrams_df = extract_ngrams(
            ngram_create_task.owner,
            sentences,
            ngram_create_task.size,
            ngram_create_task.datafile.language
        )
        ngram_create_task.progress = 2
        ngram_create_task.save()
    except Exception as e:
        ngram_create_task.status = "error"
        ngram_create_task.error = "Erro ao extrair os ngrams"
        ngram_create_task.save()
        logger.error(
            ngram_create_task.error,
            exc_info=True,
            extra={"received_args": ngram_create_task.to_mongo()}
        )
        return False


    # Salva os Ngrams
    try:
        ngrams_schema = ExtractedNGramsSchema()
        ngrams = [ngram.to_dict() for _, ngram in ngrams_df.iterrows()]

        ngrams_model: ExtractedNGramsModel = ngrams_schema.load({
            'datafile': ngram_create_task.datafile,
            'ngrams': ngrams,
            'size': ngram_create_task.size,
            'total': len(ngrams)
        })
        ngrams_model.save()

        ngram_create_task.progress = 3
        ngram_create_task.save()

    except Exception as e:
        ngram_create_task.status = "error"
        ngram_create_task.error = "Erro ao salvar os NGrams"
        ngram_create_task.save()
        logger.error(
            ngram_create_task.error,
            exc_info=True,
            extra={"received_args": ngram_create_task.to_mongo()}
        )
        return False

    ngram_create_task.status = "success"
    ngram_create_task.save()

    return True


def ngram_create_consumer(ch: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        ngram_create_task: NGramsCreateTaskModel = NGramsCreateTaskModel.objects(id=task_info["task"]).first()
        if ngram_create_task is None:
            raise Exception("Não foi encontrada nenhuma tarefa com o id " + task_info["task"])
    except Exception as e:
        logger.error(
            "Erro ao recuperar a tarefa",
            exc_info=True,
            extra={"received_args": body}
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False

    success_task = process_task(ngram_create_task)
    logger.debug("Finalizando tarefa: " + task_info["task"])

    if success_task:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return True
    else:
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False
