from datetime import datetime

import mongoengine as me
import marshmallow as ma

from marshmallow import validate
from nleaser.models.datafile import DataFileModel
from nleaser.models.nlp_extracted_data import NLPExtractedDataModel, NLPExtractedDataSchema


class NGramModel(me.EmbeddedDocument):
    content = me.StringField(required=True)
    count = me.IntField(required=True)
    relevance = me.FloatField(required=True)


class ExtractedNGramsModel(NLPExtractedDataModel):
    meta = {
        'collection': 'ngrams'
    }
    ngrams = me.fields.EmbeddedDocumentListField(
        NGramModel
    )
    total = me.fields.IntField(required=True)
    size = me.fields.IntField(required=True, min_value=1, max_value=4)


class NGramSchema(ma.Schema):
    content = ma.fields.String(required=True)
    count = ma.fields.Integer(required=True)
    relevance = ma.fields.Float(required=True)

    @ma.post_load()
    def create_ngram(self, data, **kwargs):
        return NGramModel(**data)


class ExtractedNGramsSchema(NLPExtractedDataSchema):
    ngrams = ma.fields.Nested(
        NGramSchema, many=True, required=True, unknown=ma.EXCLUDE
    )
    size = ma.fields.Integer(required=True, validate=validate.Range(1, 4))
    total = ma.fields.Integer(required=True)

    @ma.post_load
    def create_ngrams(self, data, **kwargs):
        return ExtractedNGramsModel(**data)
