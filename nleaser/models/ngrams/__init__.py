from datetime import datetime

import mongoengine as me
import marshmallow as ma
from marshmallow import validate


from nleaser.models.datafile import DataFileModel


class NGramEmbeddedDocument(me.EmbeddedDocument):
    content = me.StringField(required=True)
    count = me.IntField(required=True)


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
    size = me.fields.IntField(required=True, min_value=1, max_value=4)


class NGramSchema(ma.Schema):
    content = ma.fields.String(required=True)
    count = ma.fields.Integer(required=True)


class NGramsSchema(ma.Schema):
    datafile = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(default=datetime.now)
    ngrams = ma.fields.Nested(
        NGramSchema, required=True, many=True, unknown=ma.EXCLUDE
    )
    size = ma.fields.Integer(required=True, validate=validate.Range(1, 4))
