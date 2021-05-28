from datetime import datetime

import mongoengine as me
import marshmallow as ma
from marshmallow import validate


from nleaser.models.datafile import DataFileModel


class NGramEmbeddedDocument(me.EmbeddedDocument):
    content = me.StringField(required=True)
    count = me.IntField(required=True)
    relevance = me.FloatField(required=True)


class NGramsModel(me.Document):
    meta = {
        'collection': 'ngrams'
    }

    datafile = me.ReferenceField(
        DataFileModel, required=True, reverse_delete_rule=me.CASCADE
    )
    created_at = me.fields.DateTimeField(default=datetime.now)
    ngrams = me.fields.EmbeddedDocumentListField(
        NGramEmbeddedDocument
    )
    total = me.fields.IntField(required=True)
    size = me.fields.IntField(required=True, min_value=1, max_value=4)


class NGramSchema(ma.Schema):
    content = ma.fields.String(required=True)
    count = ma.fields.Integer(required=True)
    relevance = ma.fields.Float(required=True)

    @ma.post_load
    def create_ngram(self, data, **kwargs):
        return NGramEmbeddedDocument(**data)


class NGramsSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE

    datafile = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(default=datetime.now)
    ngrams = ma.fields.Nested(
        NGramSchema, required=True, many=True, unknown=ma.EXCLUDE
    )
    size = ma.fields.Integer(required=True, validate=validate.Range(1, 4))
    total = ma.fields.Integer(required=True)

    @ma.pre_load
    def prepare_data(self, data, **kwargs):
        data["datafile"] = str(data["datafile"].id) if type(data["datafile"]) is DataFileModel else str(data["datafile"])
        if "created_at" in data:
            data["created_at"] = data["created_at"].isoformat() if type(data["created_at"])  is datetime else str(data["created_at"])
        return data

    @ma.post_load
    def create_ngrams(self, data, **kwargs):
        return NGramsModel(**data)