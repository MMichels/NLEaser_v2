import mongoengine as me
import marshmallow as ma
from marshmallow import validate

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks import TaskModel, TaskSchema


class NGramsCreateTaskModel(TaskModel):
    task_name = me.fields.StringField(default="ngrams_create")
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    size = me.fields.IntField(required=True, min_value=1, max_value=4)
    total = me.fields.IntField(default=1)


class NGramsCreateTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="ngrams_create")
    datafile = ma.fields.String(required=True)
    size = ma.fields.Integer(required=True, validation=validate.Range(1, 4))
    total = ma.fields.Integer(default=1)

    @ma.pre_load()
    def prepare_data(self, data, **kwargs):
        data["owner"] = str(data["owner"].id) if data["owner"] else ""
        data["datafile"] = str(data["datafile"].id) if data["datafile"] else ""
        return data

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return NGramsCreateTaskModel(**data)
