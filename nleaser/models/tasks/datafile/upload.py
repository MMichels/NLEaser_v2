import mongoengine as me
import marshmallow as ma

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks import TaskModel, TaskSchema


class DataFileUploadTaskModel(TaskModel):
    meta = {
        'allow_inheritance': True
    }

    task_name = me.fields.StringField(default="datafile_import")
    datafile: DataFileModel = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)


class DataFileUploadTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="datafile_import")
    datafile = ma.fields.String(required=True)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return DataFileUploadTaskModel(**data)
