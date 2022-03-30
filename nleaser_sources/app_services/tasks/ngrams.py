from nleaser_models.datafile import DataFileModel
from nleaser_models.tasks.ngrams import NGramsCreateTaskSchema, NGramsCreateTaskModel
from nleaser_models.user import UserModel

from . import BaseTaskService


class NGramsCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(
            user,
            NGramsCreateTaskModel,
            "NLEaser.nleaser_worker_ngrams_create"
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
