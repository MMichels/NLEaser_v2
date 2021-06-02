from nleaser.models.datafile import DataFileModel
from nleaser.models.nlp_extracted_data.ner import NerResumeModel, NerResumeSchema


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
            "$unwind": "extracted_entities"
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
                "extracted_entities": {"$push": "extracted_entities"}
            }
        }
    ]
    try:
        ner_resume = NerResumeModel.objects().aggregate(
            search_pipe, allowDiskUser=True
        ).next()
        ner_resume_model = NerResumeSchema().load(ner_resume)
        return ner_resume_model
    except:
        return None


def delete_ner_resume_from_datafile(datafile: DataFileModel) -> bool:
    deleted = NerResumeModel.objects(
        datafile=datafile
    ).delete()
    return deleted > 0
