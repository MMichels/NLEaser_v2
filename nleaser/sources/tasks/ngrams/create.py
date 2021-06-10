from nleaser.models.datafile import DataFileModel
from nleaser.models.tasks.ngrams.create import NGramsCreateTaskSchema, NGramsCreateTaskModel
from nleaser.models.user import UserModel

from nleaser.sources.tasks import BaseTaskService


class NGramsCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(
            user,
            NGramsCreateTaskModel,
            "NLEaser.ngrams_create"
        )
        self.schema = NGramsCreateTaskSchema()

    def create(self, datafile: DataFileModel, size: int) -> NGramsCreateTaskModel:
        model: NGramsCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
            "size": size
        })
        model.save()
        super().create(str(model.id))
        return model
