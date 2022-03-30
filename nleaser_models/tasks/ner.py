import mongoengine as me
import marshmallow as ma


from nleaser_models.datafile import DataFileModel
from . import TaskModel, TaskSchema


class NerResumeCreateTaskModel(TaskModel):
    task_name = me.fields.StringField(default="ner_resume_create")
    datafile = me.fields.ReferenceField(DataFileModel, required=True, reverse_delete_rule=me.CASCADE)
    total = me.fields.IntField(default=1)


class NerResumeCreateTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="ner_resume_create")
    datafile = ma.fields.String(required=True)
    total = ma.fields.Integer(default=1)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return NerResumeCreateTaskModel(**data)