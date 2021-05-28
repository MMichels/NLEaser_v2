from nleaser.models.datafile import DataFileModel
from nleaser.models.ngrams import NGramsModel, NGramsSchema


def get_ngrams_from_datafile(datafile: DataFileModel, skip: int, limit: int, order_by: str, order_ascending: bool) -> NGramsModel:
    search_pipeline = [
        {
            "$match": {
                'datafile': datafile.id
            }
        },
        {
            "$unwind": "$ngrams"
        },
        {
            "$sort": {
                "ngrams.{}".format(order_by): 1 if order_ascending else -1
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
                "size": {"$first": "$size"},
                "ngrams": {"$push": "$ngrams"}
            }
        }
    ]
    try:
        ngram = NGramsModel.objects().aggregate(search_pipeline, allowDiskUse=True).next()
        ngram_model = NGramsSchema().load(ngram)

        return ngram_model
    except Exception as e:
        return None


def delete_ngrams_from_datafile(datafile: DataFileModel) -> bool:
    deleted = NGramsModel.objects(
        datafile=datafile
    ).delete()
    return deleted > 0

