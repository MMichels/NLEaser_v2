from typing import List

from nleaser_models.datafile import DataFileModel
from nleaser_models.sentence import SentenceModel


def list_sentences_from_datafile(datafile: DataFileModel, skip: int, limit: int) -> List[SentenceModel]:
    sentences = SentenceModel.objects(
        datafile=datafile
    ).skip(skip).limit(limit)
    return sentences


def delete_sentences_from_datafile(datafile: DataFileModel) -> bool:
    deleted = SentenceModel.objects(datafile=datafile).delete()

    return deleted > 0
