from datetime import datetime

import mongoengine as me
import marshmallow as ma

from nleaser.models.user import UserModel


class TasksQuerySet(me.QuerySet):
    def __init__(self, document, collection):
        super().__init__(document, collection)
        self.no_sub_classes()


class TaskModel(me.Document):
    meta = {
        'collection': 'task',
        'allow_inheritance': True,
        'queryset_class': TasksQuerySet
    }

    owner = me.fields.ReferenceField(UserModel, required=True)
    created_at = me.fields.DateTimeField(default=datetime.now)
    task_name = me.fields.StringField(required=True)
    status = me.fields.StringField(choices=["queued", "in_progress", "success", "error"], required=True,
                                   default="queued")
    error = me.fields.StringField(required=False, default="")
    total = me.fields.IntField(required=True)
    progress = me.fields.IntField(required=False, default=0)


class TaskSchema(ma.Schema):
    owner = ma.fields.String(required=True)
    id = ma.fields.String(required=True, dump_only=True)
    created_at = ma.fields.DateTime(default=datetime.now)
    task_name = ma.fields.String(required=True)
    status = ma.fields.String(default="queued",
                              validate=ma.validate.OneOf(["queued", "in_progress", "success", "error"]))
    error = ma.fields.String(required=False, default="")
    total = ma.fields.Integer(required=True)
    progress = ma.fields.Integer(required=False, default=0)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return TaskModel(**data)
