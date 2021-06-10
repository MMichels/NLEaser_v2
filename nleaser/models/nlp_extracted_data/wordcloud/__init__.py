from datetime import datetime
import mongoengine as me
import marshmallow as ma


from nleaser.models.nlp_extracted_data import NLPExtractedDataModel, NLPExtractedDataSchema


class WordcloudModel(NLPExtractedDataModel):
    meta = {
        "collection": "wordcloud"
    }
    base64_image = me.fields.StringField(required=True)


class WordcloudSchema(NLPExtractedDataSchema):
    base64_image = ma.fields.String(required=True)

    @ma.post_load
    def create_wordcloud(self, data, **kwargs):
        return WordcloudModel(**data)
