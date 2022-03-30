import json
from typing import List, Union

from pandas import DataFrame

from nleaser_models.datafile import DataFileModel
from nleaser_models.tasks.datafile import DataFileUploadTaskModel
from nleaser_models.tasks.sentence import SaveSentenceTaskModel, SentenceSaveTaskSchema
from nleaser_sources.logger import create_logger
from nleaser_sources.rabbit.producer import RabbitProducer
from nleaser_sources.services.cipher import load_cipher

logger = create_logger(__name__)


# TODO: Refatorar esse método para que a importação seja realizada no nivel da SentenceSaveTaskService
def import_sentences_from_df(df: DataFrame, datafile: DataFileModel,
                             datafile_import_task: DataFileUploadTaskModel) -> None:
    logger.info("Importando sentenças", extra={"received_args": {
        "datafile": datafile.id
    }})

    user = datafile.owner
    cipher = load_cipher(user)

    datafile_import_task.status = "queued"
    datafile_import_task.save()
    text_column = datafile.text_column
    try:

        schema = SentenceSaveTaskSchema()
        producer = RabbitProducer("NLEaser.nleaser_worker_sentence_import")
        for index, row in df.iterrows():
            sentence_import_task: SaveSentenceTaskModel = schema.load({
                "owner": str(datafile.owner.id),
                "datafile": str(datafile.id),
                "parent": str(datafile_import_task.id),
                "total": 1,
                "content": cipher.encrypt(str(row[text_column]).encode()).decode(),
                "index": index
            })
            sentence_import_task.save()
            producer.send_message(json.dumps({
                "task": str(sentence_import_task.id)
            }))
    except Exception as e:
        datafile_import_task.status = "error"
        datafile_import_task.error = "Erro desconhecido ao importar as sentenças"
        datafile_import_task.save()
        logger.error(
            "Erro ao importar sentenças do dataframe",
            exc_info=True,
            extra={"received_args": {
                "datafile": datafile.id,
                "upload": datafile_import_task.id,
                "text_column": text_column
            }}
        )


def list_sentences_from_datafile(datafile: DataFileModel, skip: int, limit: int) -> Union[List[SaveSentenceTaskModel], int]:
    sentences = list_sentences_from_datafile(datafile, skip, limit)
    cipher = load_cipher(datafile.owner)
    for s in sentences:
        s.content = cipher.decrypt(s.content.encode()).decode()
        s.pre_processed_content = cipher.decrypt(s.pre_processed_content.encode()).decode()

    return sentences, sentences.count()