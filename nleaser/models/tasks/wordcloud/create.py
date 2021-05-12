import mongoengine as me
import marshmallow as ma

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks import TaskModel, TaskSchema


class WordcloudCreateTaskModel(TaskModel):
    task_name = me.fields.StringField(default="wordcloud_create")
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    total = me.fields.IntField(default=1)


class WordcloudCreateTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="wordcloud_create")
    datafile = ma.fields.String(required=True)
    total = ma.fields.Int(default=1)

    @ma.pre_load()
    def prepare_data(self, data, **kwargs):
        data["owner"] = str(data["owner"].id) if data["owner"] else ""
        data["datafile"] = str(data["datafile"].id) if data["datafile"] else ""
        return data

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return WordcloudCreateTaskModel(**data)
