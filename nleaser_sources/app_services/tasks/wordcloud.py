from nleaser_models.datafile import DataFileModel
from nleaser_models.tasks.wordcloud import WordcloudCreateTaskModel, WordcloudCreateTaskSchema
from nleaser_models.user import UserModel
from . import BaseTaskService


class WordcloudCreateTaskService(BaseTaskService):
    def __init__(self, user: UserModel):
        super().__init__(user, WordcloudCreateTaskModel, "NLEaser.nleaser_worker_wordcloud_create")
        self.schema = WordcloudCreateTaskSchema()

    def create(self, datafile: DataFileModel) -> WordcloudCreateTaskModel:
        model: WordcloudCreateTaskModel = self.schema.load({
            "owner": self.user,
            "datafile": datafile,
        })
        model.save()
        super().create(str(model.id))
        return model
