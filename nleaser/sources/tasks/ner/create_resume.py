from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.ner.create_resume import NerResumeCreateTaskSchema, NerResumeCreateTaskModel
from nleaser.models.user import UserModel
from nleaser.sources.tasks import BaseTaskService


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

