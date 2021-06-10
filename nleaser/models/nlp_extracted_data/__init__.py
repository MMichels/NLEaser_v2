from datetime import datetime

import marshmallow as ma
import mongoengine as me

from nleaser.models.datafile import DataFileModel


class NLPExtractedDataModel(me.Document):
    meta = {
        'abstract': True
    }

    datafile = me.ReferenceField(
        DataFileModel, required=True, reverse_delete_rule=me.CASCADE
    )
    created_at = me.fields.DateTimeField(default=datetime.now)


class NLPExtractedDataSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE

    datafile = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(default=datetime.now)

    @ma.pre_load
    def prepare_data(self, data, **kwargs):
        data["datafile"] = str(data["datafile"].id) \
            if type(data["datafile"]) is DataFileModel \
            else str(data["datafile"])
        if "created_at" in data:
            data["created_at"] = data["created_at"].isoformat() \
                if type(data["created_at"]) is datetime \
                else str(data["created_at"])
        return data
