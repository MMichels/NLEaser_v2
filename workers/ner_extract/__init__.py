import json
import logging
from typing import List

from pandas import DataFrame
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelWrongStateError
from pika.spec import Basic

from nleaser.models.nlp_extracted_data.ner import NerResumeSchema, NerResumeModel
from nleaser.models.sentence import SentenceModel
from nleaser.models.tasks.ner.create_resume import NerResumeCreateTaskModel
from nleaser.models.user import UserModel
from nleaser.sources.nlp.ner import extract_ner_from_sentences
from nleaser.sources.secure import load_cipher

logger = logging.getLogger('ner_extract')


def extract_ner(
        user: UserModel, sentences: List[SentenceModel], language: str
) -> DataFrame:
    cipher = load_cipher(user)
    pre_processed_sentences = map(lambda x: cipher.decrypt(x.pre_processed_content.encode()).decode(), sentences)
    ner_sentences = extract_ner_from_sentences(pre_processed_sentences, language)
    return ner_sentences


def process_task(ner_create_task: NerResumeCreateTaskModel) -> bool:
    ner_create_task.status = "in_progress"
    ner_create_task.progress = 1
    ner_create_task.total = 4
    ner_create_task.save()

    try:
        sentences: List[SentenceModel] = SentenceModel.objects(
            datafile=ner_create_task.datafile
        ).all()
        ner_create_task.total += sentences.count()
        ner_create_task.save()
    except Exception as e:
        ner_create_task.error = "Erro ao importar as sentenças do arquivo"
        raise e


    try:
        # Extrai os dados de NER de cada sentença e atualiza o progresso da tarefa.
        ner_resume_for_df: DataFrame = None
        ner_resume_for_sentences = extract_ner(ner_create_task.owner, sentences, ner_create_task.datafile.language)
        for ner_resume_for_sentence in ner_resume_for_sentences:
            ner_create_task.progress += 1
            if ner_create_task.progress % 10 == 0:
                ner_create_task.save()
            ner_resume_for_df = ner_resume_for_sentence.append(ner_resume_for_df, ignore_index=True)
        ner_create_task.progress += 1 # 2 passo (processado)
        ner_create_task.save()
    except Exception as e:
        ner_create_task.error = "Erro ao extrair NER"
        raise e

    try:
        # Somatório das entidades por tipo e texto
        ner_resume_for_df = ner_resume_for_df.groupby(by=["content", "entity"]).count()
        ner_resume_for_df = ner_resume_for_df.sort_values(by=["count"], ascending=False)
        ner_resume_for_df = ner_resume_for_df.reset_index(level=["entity", "content"])
        ner_create_task.progress += 1 # 3 passo (processado 2)
        ner_create_task.save()
    except Exception as e:
        ner_create_task.error = "Erro ao realizar o somatório das entidades"
        raise e

    try:
        # Salva o resumo de entidades
        ner_resume_schema = NerResumeSchema()
        extracted_entities = [extracted_entity.to_dict() for _, extracted_entity in ner_resume_for_df.iterrows()]
        ner_resume_model: NerResumeModel = ner_resume_schema.load({
            'datafile': ner_create_task.datafile,
            'extracted_entities': extracted_entities,
            'total': len(extracted_entities)
        })
        ner_resume_model.save()

        ner_create_task.progress += 1 # 4 passo (salvo)
        ner_create_task.save()
    except Exception as e:
        ner_create_task.error = "Erro ao salvar os dados extraidos"
        raise e

    ner_create_task.status = "success"
    ner_create_task.save()
    return True


def ner_resume_create_consumer(ch: BlockingChannel, method: Basic.Deliver, properties, body: bytes):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        ner_resume_create_task: NerResumeCreateTaskModel = NerResumeCreateTaskModel.objects(id=task_info["task"]).first()
        if ner_resume_create_task is None:
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

    try:
        if ner_resume_create_task.status == "success" or \
                ner_resume_create_task.progress == ner_resume_create_task.total:
            ner_resume_create_task.status = "success"
            ner_resume_create_task.save()
            success_task = True
        else:
            success_task = process_task(ner_resume_create_task)
            logger.debug("Finalizando tarefa: " + task_info["task"])

        if success_task:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return True

    except ChannelWrongStateError:
        return False

    except Exception:
        ner_resume_create_task.status = "error"
        ner_resume_create_task.save()
        logger.error(
            ner_resume_create_task.error,
            exc_info=True,
            extra={"received_args": ner_resume_create_task.to_mongo()}
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False
