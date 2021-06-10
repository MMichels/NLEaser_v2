import base64
import json
import logging
from io import BytesIO
from typing import List

from nleaser.models.user import UserModel
from nleaser.models.sentence import SentenceModel
from nleaser.models.tasks.wordcloud.create import WordcloudCreateTaskModel
from nleaser.models.nlp_extracted_data.wordcloud import WordcloudModel, WordcloudSchema

from nleaser.sources.nlp.tfidf.wordcloud import generate_wordcloud
from nleaser.sources.secure import load_cipher

logger = logging.getLogger("_wordcloud_create")


def create_base64_wordcloud(user: UserModel, sentences: List[SentenceModel], language: str) -> bytes:
    cipher = load_cipher(user)
    pre_processed_sentences = [
        cipher.decrypt(sentence.pre_processed_content.encode()).decode()
        for sentence in sentences
    ]
    wordcloud = generate_wordcloud(pre_processed_sentences, language)
    image = wordcloud.to_image()
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    image_base64 = base64.b64encode(buffer.getvalue())
    return image_base64


def process_task(wordcloud_create_task: WordcloudCreateTaskModel) -> bool:
    # Recupera as sentenças
    wordcloud_create_task.status = "in_progress"
    wordcloud_create_task.total = 3
    wordcloud_create_task.progress = 1
    wordcloud_create_task.save()
    try:
        sentences: List[SentenceModel] = SentenceModel.objects(
            datafile=wordcloud_create_task.datafile
        ).all()
    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao importar as sentenças desse arquivo"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False

    # gera o wc em base64

    try:
        base64_image = create_base64_wordcloud(
            wordcloud_create_task.owner,
            sentences,
            wordcloud_create_task.datafile.language
        )
        wordcloud_create_task.progress += 1
        wordcloud_create_task.save()
    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao gerar o wordcloud em base64"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False

    # Salva o wc

    try:
        cipher = load_cipher(wordcloud_create_task.owner)
        schema = WordcloudSchema()
        model: WordcloudModel = schema.load({
            "datafile": wordcloud_create_task.datafile,
            "base64_image": cipher.encrypt(base64_image).decode()
        })
        model.save()
        wordcloud_create_task.progress += 1
        wordcloud_create_task.save()

    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao salvar o WordCloud"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False
    wordcloud_create_task.status = "success"
    wordcloud_create_task.save()

    return True


def wordcloud_create_consumer(ch, method, properties, body):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        wordcloud_create_task: WordcloudCreateTaskModel = \
            WordcloudCreateTaskModel.objects(id=task_info["task"]).first()
        if wordcloud_create_task is None:
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

    success_task = process_task(wordcloud_create_task)
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
