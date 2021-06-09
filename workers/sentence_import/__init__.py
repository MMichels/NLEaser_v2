import json
import logging

from mongoengine import NotUniqueError
from pika.channel import Channel

from nleaser.models.tasks.datafile.upload import DataFileUploadTaskModel
from nleaser.models.tasks.sentence.save import SaveSentenceTaskModel
from nleaser.models.sentence import SentenceModel, SentenceSchema
from nleaser.sources.secure import load_cipher

from nleaser.sources.nlp.preprocessing import tokenize, remove_token_accents, mask_token_numbers, remove_punkt

logger = logging.getLogger("sentence_import")


def preprocess_sentence(sentence: str, language: str) -> str:
    p_sentence = sentence.lower()

    tokens = tokenize(p_sentence, language)
    tokens = map(remove_token_accents, tokens)
    #tokens = map(mask_token_numbers, tokens)
    tokens = map(remove_punkt, tokens)
    tokens = map(lambda x: x.strip(), tokens)

    p_sentence = " ".join(tokens)

    return p_sentence


def process_task(save_sentence_task: SaveSentenceTaskModel) -> bool:
    # preprocessa a sentença
    cipher = load_cipher(save_sentence_task.owner)


    try:
        preprocessed_sentence = preprocess_sentence(
            cipher.decrypt(save_sentence_task.content.encode()).decode(),
            save_sentence_task.datafile.language
        )

    except Exception as e:
        save_sentence_task.status = "error"
        save_sentence_task.error = "Erro ao preprocessar a sentenca"
        save_sentence_task.save()
        logger.error(
            "Erro ao preprocessar a sentenca",
            exc_info=True,
            extra={"received_args": save_sentence_task.to_mongo()})
        return False

    # salva a sentença

    try:
        schema = SentenceSchema()
        sentence: SentenceModel = schema.load({
            "datafile": save_sentence_task.datafile,
            "index": save_sentence_task.index,
            "content": save_sentence_task.content,
            "pre_processed_content": cipher.encrypt(preprocessed_sentence.encode()).decode()
        })
        sentence.save()
    except NotUniqueError:
        pass

    except Exception as e:
        save_sentence_task.status = "error"
        save_sentence_task.error = "Erro ao salvar a sentença"
        save_sentence_task.save()
        logger.error(
            "Erro ao salvar a sentença",
            exc_info=True,
            extra={"received_args": save_sentence_task.to_mongo()})
        return False

    # Atualiza o status da tarefa
    save_sentence_task.progress = 1
    save_sentence_task.status = "success"
    save_sentence_task.save()

    return True


def sentence_preprocessor_consumer(ch: Channel, method, properties, body):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    # Recupera as informações da tarefa
    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        save_sentence_task: SaveSentenceTaskModel = SaveSentenceTaskModel.objects(id=task_info["task"]).first()
        if save_sentence_task is None:
            raise Exception("Não foi encontrada nenhuma tarefa com o id " + task_info["task"])

    except Exception as e:
        logger.error("Erro ao recuperar a tarefa", exc_info=True, extra={"received_args": body})
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False

    success_task = process_task(save_sentence_task)

    datafile_import_task = save_sentence_task.parent

    if datafile_import_task.status == "queued":
        datafile_import_task.status = "in_progress"
        datafile_import_task.save()

    DataFileUploadTaskModel.objects(
        id=datafile_import_task.id,
        progress__lt=datafile_import_task.total
    ).update_one(inc__progress=1)

    if success_task:
        ch.basic_ack(delivery_tag=method.delivery_tag)

    else:
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

    datafile_import_task.reload("progress", "total")
    if datafile_import_task.progress >= datafile_import_task.total:
        tasks_with_fail = SaveSentenceTaskModel.objects(
            parent=datafile_import_task,
            status="error"
        ).count()

        logger.debug("Tarefa de importação concluida: " + str(datafile_import_task.id))

        if tasks_with_fail > 0:
            datafile_import_task.status = "error"
            datafile_import_task.error = "Algumas das sentenças não foram importadas com sucesso"
        else:
            datafile_import_task.status = "success"

        datafile_import_task.save()

        # Exclui as tarefas de processamento (Evitar dados duplicados)
        SaveSentenceTaskModel.objects(parent=datafile_import_task, error="").delete()
        SaveSentenceTaskModel.objects(parent=datafile_import_task).update(set__content="CONTEUDO REMOVIDO")

    logger.debug("Tarefa concluida: " + task_info["task"])

    return True

