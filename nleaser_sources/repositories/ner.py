from nleaser_models.datafile import DataFileModel
from nleaser_models.nlp.ner import NerResumeModel, NerResumeSchema
from nleaser_sources.logger import create_logger


logger = create_logger(__name__)


def get_ner_resume_from_datafile(
        datafile: DataFileModel, skip: int, limit: int,
        order_by: str, order_ascending: bool) -> NerResumeModel:
    search_pipe = [
        {
            "$match": {
                'datafile': datafile.id
            }
        },
        {
            '$sort': {
              'created_at': -1
            }
        },
        {
            "$limit": 1
        },
        {
            "$unwind": "$extracted_entities"
        },
        {
            "$sort": {
                "extracted_entities.{}".format(order_by): 1 if order_ascending else -1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        },
        {
            "$group": {
                "_id": "$_id",
                "datafile": {"$first": "$datafile"},
                "created_at": {"$first": "$created_at"},
                "total": {"$first": "$total"},
                "extracted_entities": {"$push": "$extracted_entities"}
            }
        }
    ]
    try:
        ner_resume = NerResumeModel.objects().aggregate(
            search_pipe, allowDiskUse=True
        ).next()
        ner_resume_model = NerResumeSchema().load(ner_resume)
        return ner_resume_model
    except Exception as e:
        logger.error(
            "Erro recuperar NER do arquivo {}: {}".format(datafile.id, e.args[0]),
            exc_info=True,
            extra={
                "received_args": {
                    'id': datafile.id,
                    'skip': skip,
                    'limit': limit,
                    'order_by': order_by,
                    'order_ascending': order_ascending
                }
            }
        )
        return None


def delete_ner_resume_from_datafile(datafile: DataFileModel) -> bool:
    deleted = NerResumeModel.objects(
        datafile=datafile
    ).delete()
    return deleted > 0
