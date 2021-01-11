import mongoengine as me
import marshmallow as ma

from models.datafile import DataFileModel, DataFileSchema


class SentenceModel(me.Document):
    meta = {
        'collection': 'sentence'
    }
    datafile = me.fields.ReferenceField(DataFileModel, required=True)
    index = me.fields.IntField(required=True, unique_with='datafile')
    content = me.fields.StringField(required=True)
    pre_processed_content = me.fields.StringField(required=False)
    excluded = me.fields.BooleanField(default=False)


class SentenceSchema(ma.Schema):
    datafile = ma.fields.Nested(DataFileSchema, required=True)
    index = ma.fields.Integer(required=True)
    content = ma.fields.Str(required=True)
    pre_processed_content = ma.fields.Str(required=False)
    excluded = ma.fields.Boolean(default=False)

    @ma.post_load()
    def make_sentence(self, data, **kwargs):
        return SentenceModel(**data)
