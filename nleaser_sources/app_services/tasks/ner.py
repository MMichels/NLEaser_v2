from nleaser_models.datafile import DataFileModel
from nleaser_models.tasks.ner import NerResumeCreateTaskSchema, NerResumeCreateTaskModel
from nleaser_models.user import UserModel
from . import BaseTaskService


class NerResumeCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(
            user,
            NerResumeCreateTaskModel,
            "NLEaser.ner_resume_create"
        )
        self.schema = NerResumeCreateTaskSchema()

    def create(self, datafile: DataFileModel) -> NerResumeCreateTaskModel:
        model: NerResumeCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
        })
        model.save()
        super().create(str(model.id))
        return model

