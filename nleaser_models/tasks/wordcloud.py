import mongoengine as me
import marshmallow as ma

from nleaser_models.datafile import DataFileModel
from . import TaskModel, TaskSchema


class WordcloudCreateTaskModel(TaskModel):
    task_name = me.fields.StringField(default="_wordcloud_create")
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    total = me.fields.IntField(default=1)


class WordcloudCreateTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="_wordcloud_create")
    datafile = ma.fields.String(required=True)
    total = ma.fields.Int(default=1)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return WordcloudCreateTaskModel(**data)
