import mongoengine as me
import marshmallow as ma

from nleaser.models.datafile import DataFileModel


class SentenceModel(me.Document):
    meta = {
        'collection': 'sentence'
    }
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    index = me.fields.IntField(required=True, unique_with='datafile')
    content = me.fields.StringField(required=True)
    pre_processed_content = me.fields.StringField(required=False, default="")


class SentenceSchema(ma.Schema):
    datafile = ma.fields.String(required=True)
    index = ma.fields.Integer(required=True)
    content = ma.fields.Str(required=True)
    pre_processed_content = ma.fields.Str(required=False, default="")

    @ma.pre_load()
    def prepare_data(self, data, **kwargs):
        data["datafile"] = str(data["datafile"].id)
        return data

    @ma.post_load()
    def make_sentence(self, data, **kwargs):
        return SentenceModel(**data)
