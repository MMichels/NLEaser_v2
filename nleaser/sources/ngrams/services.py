from nleaser.models.datafile import DataFileModel
from nleaser.models.nlp_extracted_data.ngrams import ExtractedNGramsModel, ExtractedNGramsSchema


def get_ngrams_from_datafile(
        datafile: DataFileModel, skip: int, limit: int,
        order_by: str, order_ascending: bool
) -> ExtractedNGramsModel:
    search_pipeline = [
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
        ngrams = ExtractedNGramsModel.objects().aggregate(search_pipeline, allowDiskUse=True, batchSize=limit)
        ngram = ngrams.next()
        ngram_model = ExtractedNGramsSchema().load(ngram)

        return ngram_model
    except:
        return None


def delete_ngrams_from_datafile(datafile: DataFileModel) -> bool:
    deleted = ExtractedNGramsModel.objects(
        datafile=datafile
    ).delete()
    return deleted > 0

