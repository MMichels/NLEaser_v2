import mongoengine as me
import marshmallow as ma
from marshmallow import validate

from nleaser_models.datafile import DataFileModel
from . import TaskModel, TaskSchema


class NGramsCreateTaskModel(TaskModel):
    task_name = me.fields.StringField(default="nleaser_worker_ngrams_create")
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    size = me.fields.IntField(required=True, min_value=1, max_value=4)
    total = me.fields.IntField(default=1)


class NGramsCreateTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="nleaser_worker_ngrams_create")
    datafile = ma.fields.String(required=True)
    size = ma.fields.Integer(required=True, validation=validate.Range(1, 4))
    total = ma.fields.Integer(default=1)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return NGramsCreateTaskModel(**data)
