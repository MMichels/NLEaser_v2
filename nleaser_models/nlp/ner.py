import marshmallow as ma
import mongoengine as me

from . import NLPExtractedDataModel, NLPExtractedDataSchema


class EntityModel(me.EmbeddedDocument):
    content = me.StringField(required=True)
    entity = me.StringField(required=True)
    count = me.IntField(required=False)


class NerResumeModel(NLPExtractedDataModel):
    meta = {
        'collection': 'ner_resume'
    }
    extracted_entities = me.EmbeddedDocumentListField(
        EntityModel
    )
    total = me.fields.IntField(required=True)


class EntitySchema(ma.Schema):
    content = ma.fields.String(required=True)
    entity = ma.fields.String(required=True)
    count = ma.fields.Integer(required=False)

    @ma.post_load()
    def create_entity(self, data, **kwargs):
        return EntityModel(**data)


class NerResumeSchema(NLPExtractedDataSchema):
    extracted_entities = ma.fields.Nested(
        EntitySchema, many=True, required=True, unknow=ma.EXCLUDE
    )
    total = ma.fields.Integer(required=True)

    @ma.post_load()
    def create_ner_resume(self, data, **kwargs):
        return NerResumeModel(**data)
