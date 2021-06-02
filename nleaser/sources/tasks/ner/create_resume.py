import json

from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.ner.create_resume import NerResumeCreateTaskSchema, NerResumeCreateTaskModel
from nleaser.models.user import UserModel
from nleaser.sources.rabbit.producer import RabbitProducer
from nleaser.sources.tasks import BaseTaskService


class NerResumeCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        self.user = user
        self.schema = NerResumeCreateTaskSchema()
        self.producer = RabbitProducer("NLEaser.ner_resume_create")

    def create(self, datafile: DataFileModel) -> NerResumeCreateTaskModel:
        model: NerResumeCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
        })
        model.save()
        super().create(str(model.id))
        return model

